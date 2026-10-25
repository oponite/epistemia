"""Separate cardinality-search study; timed-out searches never mean NO."""

from collections import Counter, defaultdict
from contextlib import redirect_stdout
import csv
from datetime import datetime, timezone
from importlib.metadata import version
import io
import multiprocessing as mp
from pathlib import Path
import platform
import random
import statistics
import time
import traceback

import numpy as np

from benchmark import calibrate, fit_power, time_batch, REPEATS, MAX_CALLS
from subset_sum_all_sizes import solve, solve_hybrid, verify
from subset_sum_cardinality import solve_cardinality, solve_fibonacci, solve_fibonacci_gaps, solve_fibonacci_layers

HERE = Path(__file__).resolve().parent
SIZES = (8, 12, 16, 20)
GROUPS = ('singleton', 'pair', 'triple', 'growing', 'no_solution', 'skipped_optimum')
METHODS = ('DP', 'Hybrid', 'Cardinality', 'Fibonacci', 'FibonacciPhases', 'Verify')
COUNT_METHODS = ('DPCount', 'AscendingCount', 'FibonacciPhasesCount', 'FibonacciLayers')
DEADLINE = 15.0


def make_input(group, n, seed):
    rng = random.Random(seed)
    target = 3 * n + 1
    if group == 'growing':
        values = sorted(rng.sample(range(1, 3 * n + 1), n))
        return values, sum(values)
    if group == 'no_solution':
        return sorted(rng.sample(range(2, 6 * n + 1, 2), n)), target
    if group == 'skipped_optimum':
        target = 5 * n + 4
        planted = {1, 6, 11, target - 18}
        pool = [x for x in range(1, target + 1, 5) if x not in planted]
        return sorted([*planted, *rng.sample(pool, n - 4)]), target
    planted = {'singleton': {target}, 'pair': {1, target - 1},
               'triple': {1, 3, target - 4}}[group]
    pool = [x for x in range(1, 6 * n + 1, 2 if group == 'triple' else 1)
            if x not in planted and x != target]
    return sorted([*planted, *rng.sample(pool, n - len(planted))]), target


def make_cases():
    cases = []
    for group, master_seed in zip(GROUPS, range(20261028, 20261034)):
        rng = random.Random(master_seed)
        for n in SIZES:
            for instance in range(5):
                seed = rng.getrandbits(64)
                values, target = make_input(group, n, seed)
                count = {'singleton': 1, 'pair': 2, 'triple': 3,
                         'growing': n, 'no_solution': None, 'skipped_optimum': 4}[group]
                case = dict(group=group, n=n, T=target, instance=instance,
                            master_seed=master_seed, instance_seed=seed, expected_cardinality=count)
                check_case(case, values)
                cases.append(case)
    return cases


def check_case(case, values):
    group, n, target = case['group'], case['n'], case['T']
    assert len(values) == n and values == sorted(set(values)) and values[0] > 0
    expected = {'singleton': 1, 'pair': 2, 'triple': 3, 'growing': n, 'no_solution': None, 'skipped_optimum': 4}[group]
    assert case['expected_cardinality'] == expected
    if group == 'singleton':
        assert target in values
    elif group == 'pair':
        assert target not in values and {1, target - 1}.issubset(values)
    elif group == 'triple':
        assert target not in values and all(x % 2 for x in values) and target % 2
        assert {1, 3, target - 4}.issubset(values)
    elif group == 'skipped_optimum':
        assert target == 5 * n + 4 and all(x % 5 == 1 for x in values)
        assert {1, 6, 11, target - 18}.issubset(values)
    elif group == 'growing':
        assert target == sum(values)
    else:
        assert target % 2 and all(x % 2 == 0 for x in values)


def measure_worker(connection, method, values, target, expected, witness):
    try:
        function = {'DP': solve, 'Hybrid': solve_hybrid, 'Cardinality': solve_cardinality,
                    'Fibonacci': solve_fibonacci, 'FibonacciPhases': solve_fibonacci_gaps, 'Verify': verify,
                    'DPCount': solve, 'AscendingCount': solve_cardinality,
                    'FibonacciPhasesCount': solve_fibonacci_gaps,
                    'FibonacciLayers': solve_fibonacci_layers}[method]
        if method == 'FibonacciLayers':
            args = (values, target)
        elif method in COUNT_METHODS:
            args = (values, target, False)
        else:
            args = (values, target, witness) if method == 'Verify' else (values, target, True)
        output = io.StringIO()
        with redirect_stdout(output):
            calls = calibrate(function, args)
        measurements = []
        for repeat in range(REPEATS):
            result, seconds = time_batch(function, args, calls)
            if method == 'Verify':
                assert result
            elif method in COUNT_METHODS:
                assert result == (None, expected)
            else:
                subset, count = result
                assert count == expected
                if expected is None:
                    assert subset is None
                else:
                    assert len(subset) == expected and verify(values, target, subset)
            measurements.append(dict(repeat=repeat, calls=calls, seconds=seconds))
        connection.send(dict(status='COMPLETE', measurements=measurements,
                             calibration=output.getvalue().strip(), error=''))
    except Exception:
        connection.send(dict(status='ERROR', measurements=[], calibration='', error=traceback.format_exc()))
    finally:
        connection.close()


def run_worker(target, args, deadline=DEADLINE):
    """Bound a complete method/input job; launch and IPC are outside call timings."""
    context = mp.get_context('spawn')
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=target, args=(sender, *args))
    started = time.perf_counter()
    process.start()
    sender.close()
    try:
        remaining = max(0, deadline - (time.perf_counter() - started))
        if receiver.poll(remaining):
            try:
                result = receiver.recv()
            except EOFError:
                result = dict(status='ERROR', measurements=[], calibration='', error='Worker exited without a result')
        else:
            result = dict(status='TIMEOUT', measurements=[], calibration='', error='')
    finally:
        receiver.close()
        if process.is_alive():
            process.terminate()
        process.join()
        process.close()
    result['job_seconds'] = time.perf_counter() - started
    return result


def input_medians(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['group'], int(row['n']), int(row['instance']), row['method']].append(float(row['seconds']))
    return {key: statistics.median(times) for key, times in grouped.items()}


def matched_ratio(medians, group, n, numerator, denominator):
    first = {i: t for (g, size, i, method), t in medians.items()
             if (g, size, method) == (group, n, numerator)}
    second = {i: t for (g, size, i, method), t in medians.items()
              if (g, size, method) == (group, n, denominator)}
    common = sorted(first.keys() & second.keys())
    if not common:
        return None, 0
    return (statistics.median(first[i] for i in common) /
            statistics.median(second[i] for i in common)), len(common)


def summaries(rows, methods=METHODS):
    medians = input_medians(rows)
    result = {}
    for group in GROUPS:
        for method in methods:
            points = [(n, t) for (g, n, _, m), t in medians.items() if (g, m) == (group, method)]
            sizes = sorted({n for n, _ in points})
            times = [statistics.median(t for n, t in points if n == size) for size in sizes]
            slope, coefficient = fit_power(sizes, times) if len(sizes) >= 2 else (None, None)
            result[group, method] = dict(points=points, sizes=sizes, times=times,
                                         slope=slope, coefficient=coefficient)
    return result


def validate_records(rows, ledger, cases, methods=METHODS):
    expected = {(c['group'], c['n'], c['instance']): c for c in cases}
    jobs = {}
    for entry in ledger:
        key = entry['group'], int(entry['n']), int(entry['instance'])
        case = expected[key]
        method = entry['method']
        assert method in (methods if case['expected_cardinality'] is not None else tuple(m for m in methods if m != 'Verify'))
        job = (*key, method)
        assert job not in jobs
        jobs[job] = entry
        assert entry['status'] in ('COMPLETE', 'TIMEOUT', 'ERROR')
        for field in ('T', 'master_seed', 'instance_seed'):
            assert int(entry[field]) == case[field]
        count = case['expected_cardinality']
        assert entry['expected_cardinality'] in (None, '') if count is None else int(entry['expected_cardinality']) == count
    assert len(jobs) == sum(len(methods) - ('Verify' in methods and c['expected_cardinality'] is None) for c in cases)
    grouped = defaultdict(list)
    for row in rows:
        job = row['group'], int(row['n']), int(row['instance']), row['method']
        assert jobs[job]['status'] == 'COMPLETE'
        case = expected[job[:3]]
        for field in ('T', 'master_seed', 'instance_seed'):
            assert int(row[field]) == case[field]
        seconds, calls = float(row['seconds']), int(row['calls'])
        assert np.isfinite(seconds) and seconds > 0
        assert 1 <= calls <= MAX_CALLS and calls & (calls - 1) == 0
        grouped[job].append(row)
    for job, entry in jobs.items():
        records = grouped[job]
        if entry['status'] == 'COMPLETE':
            assert sorted(int(row['repeat']) for row in records) == list(range(REPEATS))
            assert len({int(row['calls']) for row in records}) == 1
        else:
            assert not records


def plot_results(summary, ledger, destination, methods=METHODS):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    figure, axes = plt.subplots(3, 2, figsize=(11, 12), layout='constrained')
    colors = dict(DP='#b35806', Hybrid='#762a83', Cardinality='#2166ac', Fibonacci='#d73058', FibonacciPhases='#008b8b', Verify='#1b7837')
    colors.update(DPCount='#b35806', AscendingCount='#2166ac', FibonacciPhasesCount='#762a83', FibonacciLayers='#008b8b')
    for group, axis in zip(GROUPS, axes.flat):
        for method in methods:
            data = summary[group, method]
            if not data['points']:
                continue
            x, y = zip(*data['points'])
            axis.scatter(x, y, color=colors[method], alpha=.3, s=15)
            axis.plot(data['sizes'], data['times'], {'Fibonacci': 's', 'FibonacciPhases': '^'}.get(method, 'o'), color=colors[method], markersize=4, label=method)
            if data['slope'] is not None:
                sizes = np.array(data['sizes'])
                axis.plot(sizes, data['coefficient'] * sizes ** data['slope'], '--', color=colors[method])
        count = sum(e['group'] == group and e['status'] == 'TIMEOUT' for e in ledger)
        axis.set(xscale='log', yscale='log', xlabel='Input size n', ylabel='Seconds per call',
                 title=f'{group.replace("_", " ").title()} ({count} timed-out jobs)')
        axis.set_xticks(SIZES, labels=[str(n) for n in SIZES])
        axis.grid(True, which='both', alpha=.2)
        axis.legend(fontsize=8)
    figure.savefig(destination, dpi=180, facecolor='white')
    plt.close(figure)


def write_report(rows, ledger, cases, metadata, destination, elapsed):
    summary, medians = summaries(rows), input_medians(rows)
    statuses = Counter(e['status'] for e in ledger)
    lines = ['# Ascending and two Fibonacci cardinality search orders', '',
             f"Run `{metadata['run_id']}` (UTC): **{len(cases)} inputs, {len(rows)} timing rows, {len(ledger)} method/input jobs**.",
             f"Statuses: {dict(statuses)}. Elapsed through plotting: **{elapsed:.2f} seconds**.", '',
             'All three searches fix every combination of k−2 indices and use two pointers on the later suffix '
             'to search exactly k elements. Cardinality tries k in ascending order. Fibonacci tries '
             '2,3,5,8,13,… until its first success, then checks every untested smaller size in ascending '
             'order. A Fibonacci success is only a candidate until those checks finish. If no Fibonacci '
             'size succeeds, it checks every remaining size before returning NO. No size is checked twice. '
             'Empty and full subsets are allowed; zero and singleton answers are handled first. '
             'FibonacciPhases holds each endpoint while searching its preceding gap ascending, then '
             'checks the endpoint only if the gap fails. Its phases are [2], [3], [4,5], [6,7,8], '
             '[9,10,11,12,13], and so on. The final partial phase is searched through the retained '
             'input count. The actual exact-k call order is 2,3,4,5,6,…, identical to Cardinality. '
             'It returns immediately at the first success. This is the revised solve_fibonacci_gaps '
             'function; older runs labeled FibonacciGaps measured the earlier endpoint-first order. '
             'None of these three searches uses DP fallback or parity shortcuts.', '',
             'Five inputs per size n=8,12,16,20 in each group. Master seeds 20261028–20261033 correspond to '
             'singleton, pair, triple, growing, no-solution, and skipped-optimum groups. All 120 inputs replay the preceding Fibonacci study unchanged. The first 100 inputs '
             'replay the earlier seeds unchanged. Singleton, pair, triple, and no-solution targets are T=3n+1, with '
             'values sampled from [1,6n]. Singleton inputs contain T; pair inputs exclude T and contain {1,T−1}; '
             'triple inputs exclude T and contain only odd values including {1,3,T−4}. Impossible inputs contain '
             'only even values against the odd target. Growing inputs sample from [1,3n] and target the sum of '
             'all values, so their optimum is n. These constructions establish the expected answers independently. '
             'Skipped-optimum inputs use T=5n+4 and n distinct values congruent to 1 modulo 5 from [1,T], '
             'including {1,6,11,T−18}. Every solution must have cardinality 4 modulo 5: the planted '
             'four-element answer is optimal, and no Fibonacci size tested at n≤20 can work. '
             'The impossible family could be rejected cheaply by parity; it is a controlled test, not a hardness claim.', '',
             'These target families differ from the earlier T=n−1 study. Compare methods within each group; '
             'do not mix historical timings into ratios.', '',
             f"Python {metadata['python']}; NumPy {metadata['numpy']}; Matplotlib {metadata['matplotlib']}; {metadata['platform']}.", '',
             'Every method/input job runs in a spawned worker with a 15-second deadline covering startup, '
             'warm-up, calibration, and five repeats. Recorded call times exclude startup and IPC, and include '
             'API validation, result construction, and loop overhead. Calibration doubles batches to 20 ms '
             '(cap 65,536 calls). Method order rotates between inputs. Correctness checks are outside timed '
             'batches. Timed-out jobs contribute no partial times and never count as NO. Verification uses a '
             'DP certificate and is not measured for impossible inputs.', '',
             f"Calibration-cap reports: {sum(bool(e['calibration']) for e in ledger)}.", '',
             'Each input time is the median of five batch averages. Size times are medians across completed '
             'inputs. Ratios use the intersection of completed inputs for the two methods and divide their '
             'size medians; parentheses give the matched count. Fits use observed size medians only. '
             'Incomplete samples are biased toward jobs that completed, and are explicitly flagged below.', '']
    for group in GROUPS:
        lines += [f'## {group.replace("_", " ").title()}', '',
                  '| Method | Fitted p | Sizes | Completed / timed out / error |', '| --- | ---: | ---: | --- |']
        for method in METHODS:
            data = summary[group, method]
            counts = Counter(e['status'] for e in ledger if (e['group'], e['method']) == (group, method))
            p = f"{data['slope']:.3f}" if data['slope'] is not None else '—'
            lines.append(f"| {method} | {p} | {len(data['sizes'])} | {counts['COMPLETE']} / {counts['TIMEOUT']} / {counts['ERROR']} |")
        if any(e['status'] != 'COMPLETE' for e in ledger if e['group'] == group):
            lines += ['', '**Incomplete group: times and fits describe completed jobs only.**']
        lines += ['', 'Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciPhases (gap before endpoint).', '',
                  '| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |',
                  '| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
        for n in SIZES:
            count = next(c['expected_cardinality'] for c in cases if (c['group'], c['n']) == (group, n))
            times = []
            for method in METHODS:
                data = summary[group, method]
                lookup = dict(zip(data['sizes'], data['times']))
                times.append(f'{lookup[n]*1000:.6f}' if n in lookup else '—')
            ratios = []
            for numerator, denominator in [('Cardinality', 'FibonacciPhases'), ('Fibonacci', 'FibonacciPhases'),
                                           ('DP', 'FibonacciPhases'), ('Hybrid', 'FibonacciPhases'),
                                           ('FibonacciPhases', 'Verify')]:
                ratio, matched = matched_ratio(medians, group, n, numerator, denominator)
                ratios.append(f'{ratio:.6g} ({matched})' if ratio is not None else '— (0)')
            lines.append(f"| {n} | {count if count is not None else 'NO'} | " + ' | '.join(times + ratios) + ' |')
        lines += ['', '| n | Method | Completed | Timed out | Error |', '| ---: | --- | ---: | ---: | ---: |']
        for n in SIZES:
            for method in METHODS:
                counts = Counter(e['status'] for e in ledger if (e['group'], int(e['n']), e['method']) == (group, n, method))
                if counts:
                    lines.append(f"| {n} | {method} | {counts['COMPLETE']} | {counts['TIMEOUT']} | {counts['ERROR']} |")
        lines.append('')
    lines += ['## Limits and reproduction', '',
              'For fixed k, the straightforward search bound is O(n^(k−1)). Searching all sizes has '
              'combinatorial worst-case cost. A power-law fit over four sizes does not turn that into a '
              'polynomial guarantee. Original Fibonacci-first ordering may add searches above the minimum. '
              'FibonacciPhases performs the same exact-k searches as ascending search; its phase boundaries '
              'do not reduce the work. '
              'Small-target DP also has favorable table sizes here. No conclusion about P versus NP follows.', '',
              '![Timing comparisons by group](benchmark.png)', '',
              '[Raw times](results.csv) · [Completion and timeout ledger](ledger.csv). Faint points are input '
              'medians; opaque markers are size medians; dashed lines fit completed observations.', '',
              '```sh', '.venv/bin/python -m pytest -q experiments/subset_sum',
              '.venv/bin/python experiments/subset_sum/benchmark_cardinality.py', '```', '',
              'Each run creates a fresh UTC-stamped directory. Earlier run artifacts remain unchanged. The benchmark does not update the README, '
              'paper, site, or publication. With restricted cache access, prefix the '
              'benchmark command with `MPLCONFIGDIR=/tmp/epistemia-mpl-cache XDG_CACHE_HOME=/tmp/epistemia-cache`.', '']
    with destination.open('x') as output:
        output.write('\n'.join(lines))


def main():
    started = time.perf_counter()
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    directory = HERE / 'cardinality' / run_id
    directory.mkdir(parents=True, exist_ok=False)
    metadata = dict(run_id=run_id, python=platform.python_version(), numpy=np.__version__,
                    matplotlib=version('matplotlib'), platform=platform.platform())
    cases = make_cases()
    rows, ledger = [], []
    for index, case in enumerate(cases):
        values, target = make_input(case['group'], case['n'], case['instance_seed'])
        witness, count = solve(values, target)
        expected = case['expected_cardinality']
        assert count == expected
        if count is not None:
            assert verify(values, target, witness)
        methods = list(METHODS if expected is not None else tuple(m for m in METHODS if m != 'Verify'))
        offset = index % len(methods)
        for method in methods[offset:] + methods[:offset]:
            result = run_worker(measure_worker, (method, values, target, expected, witness))
            common = {**metadata, **case, 'method': method}
            ledger.append({**common, 'status': result['status'], 'job_seconds': result['job_seconds'],
                           'calibration': result['calibration'], 'error': result['error']})
            rows.extend({**common, **measurement} for measurement in result['measurements'])
            if result['status'] != 'COMPLETE':
                print(case['group'], case['n'], case['instance'], method, result['status'], flush=True)
        if (index + 1) % 5 == 0:
            print(f'{index + 1}/{len(cases)} inputs measured', flush=True)
    validate_records(rows, ledger, cases)
    for name, records in [('results.csv', rows), ('ledger.csv', ledger)]:
        with (directory / name).open('x', newline='') as output:
            writer = csv.DictWriter(output, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    with (directory / 'results.csv').open(newline='') as source:
        saved = list(csv.DictReader(source))
    with (directory / 'ledger.csv').open(newline='') as source:
        saved_ledger = list(csv.DictReader(source))
    validate_records(saved, saved_ledger, cases)
    plot_results(summaries(saved), saved_ledger, directory / 'benchmark.png')
    elapsed = time.perf_counter() - started
    write_report(saved, saved_ledger, cases, metadata, directory / 'REPORT.md', elapsed)
    print(f'Saved {len(rows)} timing rows in {elapsed:.2f}s: {directory}', flush=True)
    assert not any(e['status'] == 'ERROR' for e in ledger), 'Worker errors are recorded in the ledger'


if __name__ == '__main__':
    main()
