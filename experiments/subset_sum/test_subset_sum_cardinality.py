"""Independent correctness and timeout/accounting tests for cardinality search."""

from collections import Counter
import csv
import io
import multiprocessing as mp
from pathlib import Path
import random
import time

import numpy as np
import pytest

from subset_sum_all_sizes import brute_force, verify
from subset_sum_cardinality import solve_cardinality, solve_fibonacci, solve_fibonacci_gaps


@pytest.fixture(params=[solve_cardinality, solve_fibonacci, solve_fibonacci_gaps])
def solver(request):
    return request.param


@pytest.mark.parametrize('case', range(500))
def test_against_enumeration(case, solver):
    rng = random.Random(20261033 + case)
    values = sorted(rng.sample(range(1, 41), rng.randrange(13)))
    target = rng.randint(-3, sum(values) + 3)
    original = values.copy()
    expected, count = brute_force(values, target)
    for reconstruct in (False, True):
        subset, actual = solver(values, target, reconstruct)
        assert actual == count
        if reconstruct and count is not None:
            assert len(subset) == count and subset == sorted(subset)
            assert verify(values, target, subset)
        else:
            assert subset is None
    assert values == original


@pytest.mark.parametrize('values,target,expected', [
    ([], 0, ([], 0)), ([], 1, (None, None)), ([1, 2], -1, (None, None)),
    ([1, 2], 0, ([], 0)), ([5], 5, ([5], 1)), ([2, 3, 5], 5, ([5], 1)),
    ([2, 3], 5, ([2, 3], 2)), ([1, 2, 4, 7], 13, ([2, 4, 7], 3)),
    ([1, 2, 4, 8, 16, 32], 53, ([1, 4, 16, 32], 4)),
    ([1, 2, 4, 8], 15, ([1, 2, 4, 8], 4)),
    ([1, 4, 10], 8, (None, None)), ([1, 2, 4, 10], 9, (None, None)),
    ([2, 4, 8], 7, (None, None)), ([1, 2, 10**100], 3, ([1, 2], 2)),
    ([10**100], 10**100, ([10**100], 1)),
])
def test_boundaries_and_fixed_choices(values, target, expected, solver):
    original = values.copy()
    assert solver(values, target) == expected
    assert solver(values, target, False) == (None, expected[1])
    assert values == original


@pytest.mark.parametrize('values', [[2, 1], [1, 1], [0, 1], [-1, 1], [True, 2], [1, 2.0], None])
def test_invalid_inputs(values, solver):
    with pytest.raises(ValueError):
        solver(values, 0)


@pytest.mark.parametrize('target', [True, 1.0, '3', None])
def test_invalid_targets(target, solver):
    with pytest.raises(ValueError):
        solver([1, 2, 3], target)


def test_numpy_and_large_integer_sums(solver):
    values = np.array([1, 2**63, 2**63 + 2], dtype=np.uint64)
    original = values.copy()
    assert solver(values, 2**63 + 1) == ([1, 2**63], 2)
    np.testing.assert_array_equal(values, original)
    values = np.array([1, 2, 4, 8])
    assert solver(values, np.int64(15)) == ([1, 2, 4, 8], 4)


@pytest.mark.parametrize('values,target,count,order', [
    ([1, 5, 9, 13, 17, 21, 25, 29, 37, 41], 120, 4, [2, 3, 5, 8, 4]),
    ([1, 6, 11, 16, 21, 26], 34, 4, [2, 3, 5, 4]),
    ([1, 2, 4, 8, 16, 32], 63, 6, [2, 3, 5, 4, 6]),
    ([1, 2, 4, 8, 16, 32], 31, 5, [2, 3, 5, 4]),
    ([2, 4, 6, 8, 10, 12], 13, None, [2, 3, 5, 4, 6]),
    ([1, 2, 4, 8], 7, 3, [2, 3]),
    ([], 0, 0, []), ([5], 5, 1, []), ([5], -1, None, []),
])
@pytest.mark.parametrize('reconstruct', [False, True])
def test_fibonacci_candidates_and_ascending_completion(monkeypatch, values, target, count, order, reconstruct):
    import subset_sum_cardinality as search
    original = search._search_exact
    checked = []

    def traced(values, target, k, reconstruct):
        checked.append(k)
        return original(values, target, k, reconstruct)

    monkeypatch.setattr(search, '_search_exact', traced)
    subset, actual = search.solve_fibonacci(values, target, reconstruct)
    assert actual == count == brute_force(values, target)[1]
    assert checked == order and len(checked) == len(set(checked))
    if reconstruct and count is not None:
        assert len(subset) == count and verify(values, target, subset)
    else:
        assert subset is None


def test_four_element_answer_is_not_bracketed_by_five_and_eight():
    from subset_sum_cardinality import _search_exact
    values = [1, 5, 9, 13, 17, 21, 25, 29, 37, 41]
    assert _search_exact(values, 120, 5, True) == (None, None)
    assert _search_exact(values, 120, 8, True)[1] == 8
    assert solve_fibonacci(values, 120)[1] == 4


@pytest.mark.parametrize('values,target,count,order', [
    ([1, 6, 11, 16, 21, 26], 34, 4, [2, 3, 4]),
    ([1, 2, 4, 8, 16, 17], 31, 4, [2, 3, 4]),
    ([1, 2, 4, 8, 16], 31, 5, [2, 3, 4, 5]),
    ([1, 2, 4, 8, 16, 32, 64], 127, 7, list(range(2, 8))),
    ([1, 2, 4, 8, 16, 32, 64, 128], 255, 8, list(range(2, 9))),
    (list(range(2, 27, 2)), 27, None, list(range(2, 14))),
    ([], 0, 0, []), ([5], 5, 1, []), ([5], -1, None, []),
])
@pytest.mark.parametrize('reconstruct', [False, True])
def test_fibonacci_phase_ascending_order(monkeypatch, values, target, count, order, reconstruct):
    import subset_sum_cardinality as search
    exact = search._search_exact
    checked = []

    def traced(values, target, k, reconstruct):
        checked.append(k)
        return exact(values, target, k, reconstruct)

    monkeypatch.setattr(search, '_search_exact', traced)
    subset, actual = search.solve_fibonacci_gaps(values, target, reconstruct)
    assert actual == count == brute_force(values, target)[1]
    assert checked == order and len(checked) == len(set(checked))
    if reconstruct and count is not None:
        assert len(subset) == count and verify(values, target, subset)
    else:
        assert subset is None
    if values == [1, 2, 4, 8, 16, 17]:
        assert exact(values, target, 5, True)[1] == 5


def test_fibonacci_phases_cover_final_partial_phase(monkeypatch):
    import subset_sum_cardinality as search
    checked = []

    def fail(values, target, k, reconstruct):
        checked.append(k)
        return None, None

    monkeypatch.setattr(search, '_search_exact', fail)
    assert search.solve_fibonacci_gaps(list(range(1, 23)), 1000) == (None, None)
    assert checked == list(range(2, 23))


def test_replay_previous_fibonacci_inputs():
    from benchmark_cardinality import make_cases
    previous = Path(__file__).parent / 'cardinality/20261025T162619.992087Z/ledger.csv'
    with previous.open(newline='') as source:
        old = {(r['group'], int(r['n']), int(r['instance'])): r for r in csv.DictReader(source)}
    cases = make_cases()
    assert len(old) == len(cases) == 120
    for case in cases:
        saved = old[case['group'], case['n'], case['instance']]
        for field in ('T', 'master_seed', 'instance_seed'):
            assert int(saved[field]) == case[field]


def slow_worker(connection):
    time.sleep(5)
    connection.send(dict(status='COMPLETE', measurements=[], calibration='', error=''))
    connection.close()


def test_timeout_is_not_no_and_worker_is_stopped():
    from benchmark_cardinality import run_worker
    before = {p.pid for p in mp.active_children()}
    result = run_worker(slow_worker, (), deadline=.5)
    assert result['status'] == 'TIMEOUT' and result['measurements'] == []
    assert {p.pid for p in mp.active_children()} == before


@pytest.mark.parametrize('method', ['Cardinality', 'Fibonacci', 'FibonacciPhases'])
def test_real_measurement_worker(method):
    from benchmark_cardinality import measure_worker, run_worker
    result = run_worker(measure_worker, (method, [1, 2, 4, 7], 13, 3, [2, 4, 7]))
    assert result['status'] == 'COMPLETE'
    assert len(result['measurements']) == 5
    assert all(r['seconds'] > 0 for r in result['measurements'])


def test_case_construction_and_seed_replay():
    from benchmark_cardinality import check_case, make_cases, make_input
    cases = make_cases()
    assert len(cases) == 120
    assert Counter(c['group'] for c in cases) == dict.fromkeys(
        ('singleton', 'pair', 'triple', 'growing', 'no_solution', 'skipped_optimum'), 20)
    for case in cases:
        values, target = make_input(case['group'], case['n'], case['instance_seed'])
        check_case(case, values)
        assert target == case['T']
        assert (values, target) == make_input(case['group'], case['n'], case['instance_seed'])
        # Exhaustive reference on the smallest benchmark size, including full-set optima.
        if case['n'] == 8:
            assert brute_force(values, target)[1] == case['expected_cardinality']
            assert solve_cardinality(values, target)[1] == case['expected_cardinality']
            assert solve_fibonacci(values, target)[1] == case['expected_cardinality']
            assert solve_fibonacci_gaps(values, target)[1] == case['expected_cardinality']
        if case['group'] == 'skipped_optimum':
            assert brute_force(values, target)[1] == 4
            assert case['master_seed'] == 20261033
            assert all(k % 5 != 4 for k in (2, 3, 5, 8, 13) if k <= case['n'])
    previous = Path(__file__).parent / 'cardinality/20261025T154730.002061Z/ledger.csv'
    with previous.open(newline='') as source:
        old = {(r['group'], int(r['n']), int(r['instance'])): r for r in csv.DictReader(source)}
    assert len(old) == 100
    for case in cases[:100]:
        saved = old[case['group'], case['n'], case['instance']]
        for field in ('T', 'master_seed', 'instance_seed'):
            assert int(saved[field]) == case[field]


def test_ratios_use_only_matched_completed_inputs():
    from benchmark_cardinality import matched_ratio
    medians = {('pair', 8, i, 'DP'): t for i, t in enumerate([100, 1, 2, 3, 4])}
    medians.update({('pair', 8, i, 'Cardinality'): 2 for i in range(1, 5)})
    assert matched_ratio(medians, 'pair', 8, 'DP', 'Cardinality') == (1.25, 4)
    assert matched_ratio(medians, 'pair', 8, 'Cardinality', 'Verify') == (None, 0)


def fixture_records():
    from benchmark_cardinality import make_cases, METHODS
    cases = make_cases()
    rows, ledger = [], []
    for case in cases:
        for method in METHODS if case['expected_cardinality'] is not None else tuple(m for m in METHODS if m != 'Verify'):
            common = {**case, 'method': method}
            ledger.append({**common, 'status': 'COMPLETE', 'job_seconds': 1., 'calibration': '', 'error': ''})
            rows.extend({**common, 'repeat': repeat, 'calls': 8, 'seconds': .001} for repeat in range(5))
    return cases, rows, ledger


def test_accounting_completed_timeout_and_csv_roundtrip():
    from benchmark_cardinality import validate_records
    cases, rows, ledger = fixture_records()
    assert len(rows) == 3500 and len(ledger) == 700
    validate_records(rows, ledger, cases)
    job = ledger[2]
    job['status'] = 'TIMEOUT'
    rows = [r for r in rows if any(r[f] != job[f] for f in ('group', 'n', 'instance', 'method'))]
    validate_records(rows, ledger, cases)
    assert len(rows) == 3495
    saved = []
    for records in (rows, ledger):
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
        buffer.seek(0)
        saved.append(list(csv.DictReader(buffer)))
    validate_records(*saved, cases)
    with pytest.raises(AssertionError):
        validate_records(rows + [dict(rows[0])], ledger, cases)


def test_report_timeout_and_no_overwrite(tmp_path):
    from benchmark_cardinality import write_report
    cases, rows, ledger = fixture_records()
    job = ledger[2]
    job['status'] = 'TIMEOUT'
    rows = [r for r in rows if any(r[f] != job[f] for f in ('group', 'n', 'instance', 'method'))]
    metadata = dict(run_id='fixture', python='test', numpy='test', matplotlib='test', platform='test')
    path = tmp_path / 'REPORT.md'
    write_report(rows, ledger, cases, metadata, path, 1.)
    text = path.read_text()
    assert 'Incomplete group' in text and '1 (4)' in text
    assert '| 8 | Cardinality | 4 | 1 | 0 |' in text
    with pytest.raises(FileExistsError):
        write_report(rows, ledger, cases, metadata, path, 2.)
    assert path.read_text() == text
