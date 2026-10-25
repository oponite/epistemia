"""Count-only comparison of incremental layers with DP and exact-size searches."""

from collections import Counter
import csv
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
import platform
import time

import numpy as np

from benchmark_cardinality import (
    COUNT_METHODS as METHODS, GROUPS, SIZES, make_cases, make_input,
    measure_worker, run_worker, input_medians, matched_ratio, summaries,
    validate_records, plot_results,
)
from subset_sum_all_sizes import solve, verify

HERE = Path(__file__).resolve().parent


def write_report(rows, ledger, cases, metadata, destination, elapsed):
    summary, medians = summaries(rows, METHODS), input_medians(rows)
    lines = ['# Incremental partial sums: count-only performance', '',
             f"Run `{metadata['run_id']}` (UTC): **{len(cases)} inputs, {len(rows)} timing rows, {len(ledger)} jobs**.",
             f"Statuses: {dict(Counter(r['status'] for r in ledger))}. Total runtime through plotting: **{elapsed:.2f} seconds**.", '',
             'All four APIs return only the minimum count or NO. DPCount uses solve(reconstruct=False); '
             'AscendingCount uses solve_cardinality(reconstruct=False); FibonacciPhasesCount uses '
             'solve_fibonacci_gaps(reconstruct=False); FibonacciLayers uses solve_fibonacci_layers. '
             'No certificate construction or verification is timed. Expected answers and DP certificates '
             'are checked outside timing. Comparisons use fresh measurements from this run, not earlier '
             'reconstruction timings.', '',
             'The same 120 inputs and seeds are replayed: five per group at n=8,12,16,20. Master seeds '
             '20261028–20261033 correspond to singleton, pair, triple, growing, no_solution, and '
             'skipped_optimum. Singleton/pair/triple/no-solution targets are T=3n+1; growing targets '
             'are the sum of all positive values, forcing full-set answers. Skipped-optimum inputs use '
             'T=5n+4 and values congruent to 1 modulo 5 including a planted four-element solution. '
             'Impossible cases contain only even values against an odd target. These are controlled '
             'families with known answers; they do not claim difficult instances.', '',
             'Each method/input job has a 15-second worker deadline covering launch, warm-up, calibration, '
             'and five measured batches. Batches double until 20 ms or 65,536 calls. Recorded seconds '
             'are batch elapsed time divided by calls, including public validation and count-result '
             'construction but excluding launch, calibration, correctness assertions and file writing. '
             'Method order rotates between inputs. A timeout is missing data, never NO.', '',
             f"Calibration-cap limitations: {sum(bool(r['calibration']) for r in ledger)}.",
             f"Python {metadata['python']}; NumPy {metadata['numpy']}; Matplotlib {metadata['matplotlib']}; {metadata['platform']}.", '',
             'Input times are medians of five repeats; size times are medians of input times. Ratios '
             'divide medians on matched completed inputs; parentheses give their count. Fits use '
             'logarithms of observed size medians. Incomplete groups exclude unfinished jobs and may '
             'therefore favor faster instances.', '']
    for group in GROUPS:
        lines += [f'## {group.replace("_", " ").title()}', '',
                  '| Method | Fitted p | Sizes | Complete / timeout / error |',
                  '| --- | ---: | ---: | --- |']
        for method in METHODS:
            data = summary[group, method]
            counts = Counter(r['status'] for r in ledger if (r['group'], r['method']) == (group, method))
            p = f"{data['slope']:.3f}" if data['slope'] is not None else '—'
            lines.append(f"| {method} | {p} | {len(data['sizes'])} | {counts['COMPLETE']} / {counts['TIMEOUT']} / {counts['ERROR']} |")
        if any(r['status'] != 'COMPLETE' for r in ledger if r['group'] == group):
            lines += ['', '**Incomplete group: times and fits describe completed jobs only.**']
        lines += ['', 'Median milliseconds per call. Ratios greater than one favor Layers.', '',
                  '| n | Optimum | DP | Ascending | Phases | Layers | DP / Layers | Ascending / Layers | Phases / Layers |',
                  '| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
        for n in SIZES:
            count = next(c['expected_cardinality'] for c in cases if (c['group'], c['n']) == (group, n))
            times = []
            for method in METHODS:
                data = summary[group, method]
                value = dict(zip(data['sizes'], data['times'])).get(n)
                times.append(f'{value*1000:.6f}' if value is not None else '—')
            ratios = []
            for method in METHODS[:-1]:
                ratio, matched = matched_ratio(medians, group, n, method, 'FibonacciLayers')
                ratios.append(f'{ratio:.6g} ({matched})' if ratio is not None else '— (0)')
            lines.append(f"| {n} | {count if count is not None else 'NO'} | " + ' | '.join(times + ratios) + ' |')
        lines.append('')
    lines += ['## Interpretation and reproduction', '',
              'Layers reuse partial sums, retaining the earliest endpoint at each sum and cardinality. '
              'The expected O(n²T) time and O(n+T) space bounds are pseudo-polynomial in numeric T. '
              'The DP comparator has an O(nT) bound; exact-size searches remain combinatorial. '
              'Fibonacci boundaries alone do not reduce work. Fits over four small sizes are descriptions '
              'of this run, not asymptotic proofs. Large targets, sizes above 20, and layer reconstruction '
              'are not measured. No conclusion about P versus NP follows.', '',
              '![Count-only comparisons across six groups](benchmark.png)', '',
              '[Raw times](results.csv) · [Completion and timeout ledger](ledger.csv)', '',
              '```sh', '.venv/bin/python -m pytest -q experiments/subset_sum',
              'MPLCONFIGDIR=/tmp/epistemia-mpl-cache XDG_CACHE_HOME=/tmp/epistemia-cache .venv/bin/python experiments/subset_sum/benchmark_layers.py',
              '```', '', 'Each run creates a new timestamped directory; earlier artifacts are preserved.', '']
    with destination.open('x') as output:
        output.write('\n'.join(lines))


def main():
    started = time.perf_counter()
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    directory = HERE / 'layers' / run_id
    directory.mkdir(parents=True, exist_ok=False)
    metadata = dict(run_id=run_id, python=platform.python_version(), numpy=np.__version__,
                    matplotlib=version('matplotlib'), platform=platform.platform(), mode='count_only')
    cases = make_cases()
    rows, ledger = [], []
    for index, case in enumerate(cases):
        values, target = make_input(case['group'], case['n'], case['instance_seed'])
        witness, count = solve(values, target)
        assert count == case['expected_cardinality']
        assert count is None or verify(values, target, witness)
        offset = index % len(METHODS)
        for method in METHODS[offset:] + METHODS[:offset]:
            result = run_worker(measure_worker, (method, values, target, count, None))
            common = {**metadata, **case, 'method': method}
            ledger.append({**common, 'status': result['status'], 'job_seconds': result['job_seconds'],
                           'calibration': result['calibration'], 'error': result['error']})
            rows.extend({**common, **measurement} for measurement in result['measurements'])
            if result['status'] != 'COMPLETE':
                print(case['group'], case['n'], case['instance'], method, result['status'], flush=True)
        if (index + 1) % 5 == 0:
            print(f'{index + 1}/{len(cases)} inputs measured', flush=True)
    validate_records(rows, ledger, cases, METHODS)
    for name, records in [('results.csv', rows), ('ledger.csv', ledger)]:
        with (directory / name).open('x', newline='') as output:
            fields = list(records[0]) if records else [*common, 'repeat', 'calls', 'seconds']
            writer = csv.DictWriter(output, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)
    saved = list(csv.DictReader((directory / 'results.csv').open(newline='')))
    saved_ledger = list(csv.DictReader((directory / 'ledger.csv').open(newline='')))
    validate_records(saved, saved_ledger, cases, METHODS)
    plot_results(summaries(saved, METHODS), saved_ledger, directory / 'benchmark.png', METHODS)
    elapsed = time.perf_counter() - started
    write_report(saved, saved_ledger, cases, metadata, directory / 'REPORT.md', elapsed)
    print(f'Saved {len(rows)} timing rows in {elapsed:.2f}s: {directory}', flush=True)
    assert not any(r['status'] == 'ERROR' for r in ledger), 'Worker errors are recorded in the ledger'


if __name__ == '__main__':
    main()
