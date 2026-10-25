"""Correctness, branch selection, and accounting for the separate experiment."""

from collections import Counter
import csv
import io
import random

import numpy as np
import pytest

import subset_sum_all_sizes as algorithms
from subset_sum_all_sizes import brute_force, solve, solve_hybrid, verify


@pytest.mark.parametrize("case", range(500))
def test_random_all_sizes_against_enumeration(case):
    rng = random.Random(20261025 + case)
    X = sorted(rng.sample(range(1, 41), rng.randrange(13)))
    target = rng.randint(-3, sum(X) + 3)
    original = X.copy()
    expected_subset, expected_count = brute_force(X, target)
    for function in (solve, solve_hybrid):
        for reconstruct in (False, True):
            subset, count = function(X, target, reconstruct)
            assert count == expected_count
            if reconstruct and count is not None:
                assert subset == sorted(subset) and len(subset) == count
                assert verify(X, target, subset)
            else:
                assert subset is None
    if expected_count is not None:
        assert verify(X, target, expected_subset)
    assert X == original


@pytest.mark.parametrize("X,target,expected", [
    ([], 0, ([], 0)), ([], 1, (None, None)), ([], -1, (None, None)),
    ([1, 2, 3], 0, ([], 0)), ([1, 2, 3], -1, (None, None)),
    ([7], 7, ([7], 1)), ([7], 8, (None, None)),
    ([2, 3, 5, 10], 5, ([5], 1)),
    ([2, 3], 5, ([2, 3], 2)), ([2, 3, 4], 9, ([2, 3, 4], 3)),
    ([1, 2, 3, 10, 20, 30, 40], 6, ([1, 2, 3], 3)),
    ([2, 4, 8], 7, (None, None)), ([1, 2, 10**100], 3, ([1, 2], 2)),
])
def test_all_sizes_boundaries(X, target, expected):
    original = X.copy()
    for function in (solve, solve_hybrid, brute_force):
        assert function(X, target) == expected
    for function in (solve, solve_hybrid):
        assert function(X, target, False) == (None, expected[1])
    if expected[1] is not None:
        assert verify(X, target, expected[0])
    assert X == original


@pytest.mark.parametrize("X", [[2, 1], [1, 1], [0, 1], [-1, 1], [1, 2.0], [True, 2], None])
def test_invalid_instances(X):
    for function in (solve, solve_hybrid, brute_force):
        with pytest.raises(ValueError):
            function(X, 0)
    assert not verify(X, 0, [])


@pytest.mark.parametrize("target", [3.0, True, "3", None])
def test_invalid_targets(target):
    for function in (solve, solve_hybrid, brute_force):
        with pytest.raises(ValueError):
            function([1, 2, 3], target)
    assert not verify([1, 2, 3], target, [])


@pytest.mark.parametrize("subset", [None, 3, [1, 1], [1, 9], [1, 2, 3, 4], [1, 2.0], [True, 2], [[1], 2]])
def test_invalid_certificates(subset):
    assert not verify([1, 2, 3], 3, subset)


def test_verifier_accepts_empty_full_and_nonminimum_answers():
    assert verify([], 0, [])
    assert verify([1, 2, 3], 0, [])
    assert verify([1, 2, 3], 6, [3, 1, 2])
    assert verify([2, 3, 5], 5, [2, 3])
    assert solve([2, 3, 5], 5) == ([5], 1)
    assert not verify([1, 2], 1, [])


@pytest.mark.parametrize("reconstruct", [False, True])
@pytest.mark.parametrize("X,target,count", [([], 0, 0), ([1, 2, 3], 0, 0),
                                                ([2, 3, 5, 10], 5, 1), ([1, 2, 3, 4], 5, 2)])
def test_early_paths_validate_once_and_bypass_dp(monkeypatch, X, target, count, reconstruct):
    calls = []
    validate = algorithms._validate

    def checked(values, total):
        calls.append((values, total))
        validate(values, total)

    def forbidden(*args):
        pytest.fail("DP must not run on an early success")

    monkeypatch.setattr(algorithms, "_validate", checked)
    monkeypatch.setattr(algorithms, "solve", forbidden)
    subset, actual = solve_hybrid(X, target, reconstruct)
    assert actual == count and calls == [(X, target)]
    if reconstruct:
        assert len(subset) == count and sum(subset) == target
    else:
        assert subset is None


@pytest.mark.parametrize("reconstruct", [False, True])
@pytest.mark.parametrize("X,target,count", [([1, 2, 3, 10], 6, 3), ([2, 4, 8], 7, None),
                                          ([1, 2, 3], 6, 3)])
def test_fallback_invokes_dp(monkeypatch, X, target, count, reconstruct):
    calls = []

    def fallback(values, total, rebuild):
        calls.append((values, total, rebuild))
        return solve(values, total, rebuild)

    monkeypatch.setattr(algorithms, "solve", fallback)
    subset, actual = solve_hybrid(X, target, reconstruct)
    assert actual == count and calls == [(X, target, reconstruct)]
    if subset is not None:
        assert verify(X, target, subset)


def test_numpy_and_large_integer_arithmetic():
    for function in (solve, solve_hybrid, brute_force):
        X = np.array([1, 2, 3])
        original = X.copy()
        assert function(X, np.int64(6)) == ([1, 2, 3], 3)
        np.testing.assert_array_equal(X, original)
    X = np.array([1, 2**62, 2**62 + 1, 2**62 + 2], dtype=np.int64)
    original = X.copy()
    pair, count = solve_hybrid(X, 2**63 + 1)
    assert count == 2 and verify(X, 2**63 + 1, pair)
    assert all(type(value) is int for value in pair)
    np.testing.assert_array_equal(X, original)
    X = np.array([1, 2**63, 2**63 + 2], dtype=np.uint64)
    # An adjacent large target must not match a rounded NumPy singleton comparison.
    assert solve_hybrid(X, 2**63 + 1) == ([1, 2**63], 2)
    assert solve_hybrid([10**100], 10**100) == ([10**100], 1)
    assert solve_hybrid([1, 10**100, 10**100 + 1], 2 * 10**100 + 1, False) == (None, 2)


def test_generated_cases_have_independent_answers():
    from benchmark_all_sizes import check_case, make_cases, make_input

    cases = make_cases()
    assert len(cases) == 90
    assert Counter(case["group"] for case in cases) == {
        "singleton": 8, "pair": 22, "triple": 30, "no_solution": 30}
    assert not any(case["group"] == "singleton" and case["n"] == 4000 for case in cases)
    for case in cases:
        X = make_input(case["group"], case["n"], case["instance_seed"])
        check_case(case, X)
        assert X == make_input(case["group"], case["n"], case["instance_seed"])
        for function in (solve, solve_hybrid):
            subset, count = function(X, case["T"])
            assert count == case["expected_cardinality"]
            if count is not None:
                assert len(subset) == count and verify(X, case["T"], subset)
            else:
                assert subset is None


def test_group_medians_and_missing_sizes():
    from benchmark_all_sizes import summarize

    rows = [{"group": "singleton", "series": method, "n": n, "instance": instance, "seconds": seconds}
            for method in ("DP", "Hybrid", "Verify")
            for n, instance, seconds in [(100, 0, 1), (100, 0, 3), (100, 0, 5),
                                         (100, 1, 9), (200, 0, 12)]]
    rows.append({"group": "pair", "series": "DP", "n": 4000, "instance": 0, "seconds": 999})
    results = summarize(rows)
    assert results["singleton"]["DP"]["sizes"] == [100, 200]
    assert results["singleton"]["DP"]["seconds"] == [6, 12]
    assert results["singleton"]["DP"]["slope"] == pytest.approx(1)
    assert results["no_solution"]["Verify"]["sizes"] == []


def synthetic_records():
    from benchmark_all_sizes import METHODS, REPEATS, make_cases

    cases = make_cases()
    rows = [{**case, "series": method, "repeat": repeat, "calls": 8,
             "seconds": case["n"] * {"DP": 4, "Hybrid": 2, "Verify": 1}[method] / 1000000,
             "solved": int(case["expected_cardinality"] is not None),
             "cardinality": case["expected_cardinality"],
             "run_id": "fixture", "python": "test", "numpy": "test", "matplotlib": "test", "platform": "test"}
            for case in cases for method in (METHODS if case["expected_cardinality"] is not None else METHODS[:2])
            for repeat in range(REPEATS)]
    return cases, rows


def test_record_accounting_and_csv_roundtrip():
    from benchmark_all_sizes import validate_results

    cases, rows = synthetic_records()
    assert len(rows) == 1200
    validate_results(rows, cases)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    buffer.seek(0)
    validate_results(list(csv.DictReader(buffer)), cases)
    bad = [dict(row) for row in rows]
    bad[0]["repeat"] = 1
    with pytest.raises(AssertionError):
        validate_results(bad, cases)
    bad = [dict(row) for row in rows]
    bad[-1]["series"] = "Verify"
    with pytest.raises(AssertionError):
        validate_results(bad, cases)


def test_report_ratios_missing_sizes_and_no_overwrite(tmp_path):
    from benchmark_all_sizes import summarize, write_report

    cases, rows = synthetic_records()
    destination = tmp_path / "REPORT.md"
    write_report(rows, cases, summarize(rows), destination, 1.0, [])
    report = destination.read_text()
    assert "| 4000 | 0 | — | — | — | — | — | — |" in report
    assert "| 100 | 1 | 0.400000 | 0.200000 | 0.100000 | 2.000 | 4.000 | 2.000 |" in report
    assert "| 100 | 5 | 0.400000 | 0.200000 | — | 2.000 | — | — |" in report
    with pytest.raises(FileExistsError):
        write_report(rows, cases, summarize(rows), destination, 2.0, [])
    assert destination.read_text() == report
