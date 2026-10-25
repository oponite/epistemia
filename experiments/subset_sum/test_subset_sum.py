import csv
import math
from collections import Counter, defaultdict
import random

import numpy as np
import pytest

from subset_sum import brute_force, solve, solve_hybrid, solve_pair, verify


@pytest.mark.parametrize("case", range(500))
def test_random_against_enumeration(case):
    rng = random.Random(20261025 + case)
    n = rng.randrange(13)
    X = sorted(rng.sample(range(1, 41), n))
    T = rng.randint(-3, n - 1 if case % 2 == 0 else sum(X) + 3)
    original = X.copy()
    expected_subset, expected_count = brute_force(X, T)
    if expected_subset is not None:
        assert verify(X, T, expected_subset)
    for function in (solve, solve_hybrid):
        for reconstruct in (False, True):
            subset, count = function(X, T, reconstruct=reconstruct)
            assert count == expected_count
            if reconstruct:
                assert (subset is None) == (expected_subset is None)
                if subset is not None:
                    assert len(subset) == count
                    assert subset == sorted(subset)
                    assert verify(X, T, subset)
            else:
                assert subset is None
    pair, count = solve_pair(X, T)
    assert (count == 2) == (expected_count == 2)
    if count == 2:
        assert len(pair) == 2 and pair == sorted(pair) and verify(X, T, pair)
    else:
        assert pair is None and count is None
    assert X == original


@pytest.mark.parametrize(
    "X,T,count",
    [
        ([1, 2, 3], 0, None),
        ([1, 2, 3], -2, None),
        ([], 3, None),
        ([1], 1, None),
        ([1, 2], 3, None),
        ([2, 5, 9], 5, None),
        ([2, 3, 5, 9], 5, 2),
        ([1, 2, 3], 6, None),
        ([2, 4, 8], 7, None),
        ([2, 5, 9], 4, None),
        ([1, 2, 5, 8], 3, 2),
        ([1, 2, 10], 3, 2),
        ([1, 2, 3, 4, 8], 5, 2),
        ([1, 2, 10**100], 3, 2),
        (list(range(1, 21)), 19, 2),
        ([1, 2, 3, 10, 20, 30, 40], 6, 3),
    ],
)
def test_boundaries(X, T, count):
    original = X.copy()
    for function in (solve, solve_hybrid):
        for reconstruct in (False, True):
            subset, actual = function(X, T, reconstruct)
            assert actual == count == brute_force(X, T)[1]
            if subset is not None:
                assert verify(X, T, subset)
    pair, pair_count = solve_pair(X, T)
    assert pair_count == (2 if count == 2 else None)
    if pair is not None:
        assert verify(X, T, pair)
    assert X == original


@pytest.mark.parametrize("X", [[2, 1], [1, 1], [0, 1], [-1, 1], [1, 2.0], [True, 2], None])
def test_invalid_instances(X):
    for function in (solve, solve_pair, solve_hybrid, brute_force):
        with pytest.raises(ValueError):
            function(X, 3)
    assert not verify(X, 3, [1, 2])


@pytest.mark.parametrize("T", [3.0, True, "3", None])
def test_invalid_target(T):
    for function in (solve, solve_pair, solve_hybrid, brute_force):
        with pytest.raises(ValueError):
            function([1, 2, 3], T)
    assert not verify([1, 2, 3], T, [1, 2])


@pytest.mark.parametrize("S", [None, 3, [], [3], [1, 1], [1, 3], [1, 9], [1, 2, 3, 4], [1, 2.0], [True, 2], [[1], 2]])
def test_reject_certificates(S):
    assert not verify([1, 2, 3, 4], 3, S)


def test_verification_accepts_nonminimum_and_unsorted_certificates():
    X = [1, 2, 3, 4, 10]
    assert solve(X, 6)[1] == 2
    assert verify(X, 6, [3, 1, 2])


def test_numpy_integer_inputs_and_python_integer_sum():
    for function in (solve, solve_pair, solve_hybrid):
        assert function(np.array([1, 2, 10]), np.int64(3)) == ([1, 2], 2)
    X = np.array([1, 2**62, 2**62 + 1, 2**62 + 2], dtype=np.int64)
    assert verify(X, 2**63 + 1, X[1:3])
    original = X.copy()
    for function in (solve_pair, solve_hybrid):
        subset, count = function(X, 2**63 + 1)
        assert count == 2 and verify(X, 2**63 + 1, subset)
        assert all(type(value) is int for value in subset)
    np.testing.assert_array_equal(X, original)
    assert solve_hybrid(X, 2**63 + 1, False) == (None, 2)


def test_large_python_integer_pair():
    X = [1, 10**100, 10**100 + 1]
    original = X.copy()
    for function in (solve_pair, solve_hybrid):
        assert function(X, 2 * 10**100 + 1) == (X[1:], 2)
    assert X == original


@pytest.mark.parametrize("reconstruct", [False, True])
def test_hybrid_pair_bypasses_dp(monkeypatch, reconstruct):
    import subset_sum

    def forbidden(*args):
        pytest.fail("DP must not run after finding an optimal pair")

    monkeypatch.setattr(subset_sum, "solve", forbidden)
    assert solve_hybrid([1, 2, 3, 4, 10], 5, reconstruct) == (
        [1, 4] if reconstruct else None, 2)


@pytest.mark.parametrize("X,T,count", [
    ([1, 2, 3, 10, 20, 30, 40], 6, 3),
    ([2, 4, 8], 7, None),
    ([1, 2, 3], 6, None),
])
@pytest.mark.parametrize("reconstruct", [False, True])
def test_hybrid_pair_failure_invokes_dp(monkeypatch, X, T, count, reconstruct):
    import subset_sum

    calls = []

    def fallback(values, target, rebuild):
        calls.append((values, target, rebuild))
        return solve(values, target, rebuild)

    monkeypatch.setattr(subset_sum, "solve", fallback)
    assert solve_pair(X, T) == (None, None)
    subset, actual = solve_hybrid(X, T, reconstruct)
    assert actual == count
    assert calls == [(X, T, reconstruct)]
    if subset is not None:
        assert verify(X, T, subset)


@pytest.mark.parametrize("exponent", [1, 2])
def test_benchmark_power_fit(exponent):
    from benchmark import fit_power

    sizes = np.array([100, 250, 500, 1000], dtype=float)
    slope, coefficient = fit_power(sizes, 0.001 * sizes**exponent)
    assert slope == pytest.approx(exponent)
    assert coefficient == pytest.approx(0.001)


def test_benchmark_medians_and_independent_c_series():
    from benchmark import summarize

    rows = [
        {"series": "C solve (successful)", "n": n, "instance": instance, "seconds": seconds, "solved": 1}
        for n, instance, seconds in [
            (10, 0, 1), (10, 0, 3), (10, 0, 5),
            (10, 1, 9), (20, 0, 12),
        ]
    ]
    rows += [{"series": "B reconstruct", "n": 40, "instance": 0,
              "seconds": 1000, "solved": 1}]
    for label in ("C pair", "C hybrid", "C verify"):
        rows += [{**row, "series": label} for row in rows[:5]]
    summaries = summarize(rows)
    assert summaries["B reconstruct"]["sizes"] == [40]
    for label in ("C solve (successful)", "C pair", "C hybrid", "C verify"):
        assert summaries[label]["sizes"] == [10, 20]
        assert summaries[label]["seconds"] == [6, 12]
        assert summaries[label]["slope"] == pytest.approx(1)


def test_batch_time_normalization(monkeypatch):
    import benchmark

    ticks = iter([10.0, 10.4])
    monkeypatch.setattr(benchmark.time, "perf_counter", lambda: next(ticks))
    calls = []

    def operation(value):
        calls.append(value)
        return len(calls)

    result, seconds = benchmark.time_batch(operation, (7,), 4)
    assert result == 4 and calls == [7] * 4
    assert seconds == pytest.approx(0.1)


def test_report_uses_size_median_ratios(capsys):
    from benchmark import print_report

    rows = [
        {"series": label, "n": 100, "instance": instance, "seconds": seconds}
        for label, measurements in [
            ("C solve (successful)", [0.012, 0.004, 0.002]),
            ("C pair", [0.002, 0.001, 0.003]),
            ("C hybrid", [0.003, 0.004, 0.002]),
            ("C verify", [0.001, 0.002, 0.0005]),
        ]
        for instance, seconds in enumerate(measurements)
    ]
    print_report(rows)
    report = capsys.readouterr().out
    assert "| 100 | 4.000000 | 2.000000 | 3.000000 | 1.000000 |" in report
    assert "| 100 | 2.000 | 1.333 | 4.000 | 2.000 | 3.000 |" in report


@pytest.mark.parametrize("per_call,expected,limited", [(0.01, 2, False), (0.001, 4, True)])
def test_calibration_doubling_and_cap(monkeypatch, capsys, per_call, expected, limited):
    import benchmark

    batches, warmups = [], []

    def operation(values):
        warmups.append(values)

    def measured(function, args, calls):
        batches.append(calls)
        return None, per_call

    monkeypatch.setattr(benchmark, "time_batch", measured)
    monkeypatch.setattr(benchmark, "MAX_CALLS", 4)
    assert benchmark.calibrate(operation, ([1, 2, 3],)) == expected
    assert batches == ([1, 2] if expected == 2 else [1, 2, 4])
    assert warmups == [[1, 2, 3]]
    assert ("CALIBRATION LIMIT" in capsys.readouterr().out) == limited


def test_recorded_results():
    """Replay saved seeds and check accounting without requiring a speedup."""
    from benchmark import HERE, INSTANCES, MAX_CALLS, REPEATS, SEED, SERIES

    with (HERE / "results.csv").open(newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames
        rows = list(reader)
    with (HERE / "baseline/results.csv").open(newline="") as source:
        reader = csv.DictReader(source)
        assert reader.fieldnames == fields
        baseline = list(reader)
    assert len(rows) == 1000
    assert Counter(row["series"] for row in rows) == {
        label: 100 if label == "A solve" else 150 for label in SERIES
    }
    old_seeds = {(row["n"], row["T"], row["instance"]): row["instance_seed"]
                 for row in baseline}
    rng = random.Random(SEED)
    expected = {}
    for experiment, sizes in (("A", (1000, 10000, 100000, 1000000)),
                              ("B", (100, 250, 500, 1000, 2000, 4000))):
        for size in sizes:
            n, target = (100, size) if experiment == "A" else (size, size - 1)
            for instance in range(INSTANCES):
                seed = rng.getrandbits(64)
                key = (str(n), str(target), str(instance))
                assert old_seeds[key] == str(seed)
                upper = target - 1 if experiment == "A" else 3 * n
                X = sorted(random.Random(seed).sample(range(1, upper + 1), n))
                subset, count = solve(X, target, reconstruct=experiment == "B")
                if subset is not None:
                    assert verify(X, target, subset)
                if experiment == "B":
                    assert count == 2
                    for function in (solve_pair, solve_hybrid):
                        pair, pair_count = function(X, target)
                        assert pair_count == 2 and verify(X, target, pair)
                expected[key] = (seed, count, sum(value < target for value in X),
                                 sum(target - value + 1 for value in X if value < target))
    groups = defaultdict(list)
    for row in rows:
        key = (row["n"], row["T"], row["instance"])
        seed, count, retained, updates = expected[key]
        assert int(row["master_seed"]) == SEED
        assert int(row["instance_seed"]) == seed
        assert int(row["m"]) == retained
        assert int(row["solved"]) == int(count is not None)
        assert row["cardinality"] == (str(count) if count is not None else "")
        seconds, calls = float(row["seconds"]), int(row["calls"])
        assert math.isfinite(seconds) and seconds > 0
        if row["series"].startswith("C"):
            assert row["experiment"] == "C"
            assert 1 <= calls <= MAX_CALLS and calls & (calls - 1) == 0
            assert int(row["reconstruct"]) == int(row["series"] != "C verify")
            if row["series"] != "C solve (successful)":
                updates = 0
        else:
            assert calls == 1
        assert int(row["dp_updates"]) == updates
        groups[(row["series"], *key)].append(row)
    for group in groups.values():
        assert sorted(int(row["repeat"]) for row in group) == list(range(REPEATS))
        assert len({row["calls"] for row in group}) == 1
