"""Seeded measurements; run directly to write results.csv beside this file."""

import csv
from importlib.metadata import version
from pathlib import Path
import platform
import random
import statistics
import time

import numpy as np

from subset_sum import solve, solve_hybrid, solve_pair, verify

SEED = 20261025
INSTANCES = 5
REPEATS = 5
MIN_BATCH_SECONDS = 0.020
MAX_CALLS = 65536
HERE = Path(__file__).resolve().parent
SERIES = {
    "A solve": ("T", 1),
    "B count only": ("n", 2),
    "B reconstruct": ("n", 2),
    "C solve (successful)": ("n", 2),
    "C pair": ("n", 1),
    "C hybrid": ("n", 1),
    "C verify": ("n", 1),
}


def fit_power(sizes, seconds):
    """Least-squares fit t = coefficient * size**slope, in log space."""
    slope, intercept = np.polyfit(np.log(sizes), np.log(seconds), 1)
    return float(slope), float(np.exp(intercept))


def summarize(rows):
    """Median repeats per instance, then median instances per size."""
    summaries = {}
    for label, (axis, expected) in SERIES.items():
        grouped = {}
        for row in rows:
            matches = row["series"] == label
            if matches:
                key = (int(row[axis]), int(row["instance"]))
                grouped.setdefault(key, []).append(float(row["seconds"]))
        points = [(size, statistics.median(times)) for (size, _), times in grouped.items()]
        sizes = sorted({size for size, _ in points})
        medians = [statistics.median(t for x, t in points if x == size) for size in sizes]
        slope, coefficient = fit_power(sizes, medians) if len(sizes) >= 2 else (None, None)
        summaries[label] = {
            "sizes": sizes, "seconds": medians, "points": points,
            "slope": slope, "coefficient": coefficient, "expected": expected,
        }
    return summaries


def print_report(rows):
    """Print reproducible Markdown tables from the same medians as the plot."""
    summaries = summarize(rows)
    print("| Series | Measured p | Reference p |")
    print("| --- | ---: | ---: |")
    for label, summary in summaries.items():
        slope = summary["slope"]
        if slope is None:
            continue
        print(f"| {label} | {slope:.3f} | {summary['expected']} |")
    labels = ("C solve (successful)", "C pair", "C hybrid", "C verify")
    times = {label: dict(zip(summaries[label]["sizes"], summaries[label]["seconds"]))
             for label in labels}
    sizes = sorted(set.intersection(*(set(times[label]) for label in labels)))
    print("\nC times in milliseconds per call:\n")
    print("| n | DP | Pair | Hybrid | Verify |")
    print("| ---: | ---: | ---: | ---: | ---: |")
    for n in sizes:
        print(f"| {n} | " + " | ".join(f"{times[label][n] * 1000:.6f}" for label in labels) + " |")
    print("\nRatios of unrounded size medians (not medians of per-instance ratios):\n")
    print("| n | DP / pair | DP / hybrid | DP / verify | Pair / verify | Hybrid / verify |")
    print("| ---: | ---: | ---: | ---: | ---: | ---: |")
    for n in sizes:
        dp, pair, hybrid, verification = (times[label][n] for label in labels)
        ratios = (dp / pair, dp / hybrid, dp / verification, pair / verification, hybrid / verification)
        print(f"| {n} | " + " | ".join(f"{ratio:.3f}" for ratio in ratios) + " |")


def time_batch(function, args, calls):
    """Return the last result and seconds per call, including loop overhead."""
    before = time.perf_counter()
    for _ in range(calls):
        result = function(*args)
    seconds = (time.perf_counter() - before) / calls
    return result, seconds


def calibrate(function, args):
    """Warm up, then choose a batch size; calibration is not a measurement row."""
    function(*args)
    calls = 1
    while True:
        _, seconds = time_batch(function, args, calls)
        if seconds * calls >= MIN_BATCH_SECONDS:
            return calls
        if calls == MAX_CALLS:
            print(f"CALIBRATION LIMIT: {function.__name__}, n={len(args[0])}: "
                  f"{calls} calls below {MIN_BATCH_SECONDS * 1000:.0f} ms", flush=True)
            return calls
        calls *= 2


def main():
    started = time.perf_counter()
    rng = random.Random(SEED)
    rows = []
    metadata = {
        "master_seed": SEED, "python": platform.python_version(),
        "numpy": np.__version__, "matplotlib": version("matplotlib"),
        "platform": platform.platform(), "machine": platform.machine(),
        "processor": platform.processor(),
    }
    for experiment, sizes in (("A", (1000, 10000, 100000, 1000000)),
                              ("B", (100, 250, 500, 1000, 2000, 4000))):
        for size in sizes:
            n, target = (100, size) if experiment == "A" else (size, size - 1)
            for instance in range(INSTANCES):
                instance_seed = rng.getrandbits(64)
                instance_rng = random.Random(instance_seed)
                upper = target - 1 if experiment == "A" else 3 * n
                X = sorted(instance_rng.sample(range(1, upper + 1), n))
                Y = [value for value in X if value < target]
                common = {
                    **metadata, "experiment": experiment, "n": n, "T": target,
                    "m": len(Y), "instance": instance, "instance_seed": instance_seed,
                    "dp_updates": sum(target - value + 1 for value in Y),
                }
                modes = (False,) if experiment == "A" else (False, True)
                expected_count = None
                witness = None
                for reconstruct in modes:
                    warm_subset, count = solve(X, target, reconstruct)
                    if reconstruct:
                        assert count == expected_count
                        witness = warm_subset
                    else:
                        expected_count = count
                    if warm_subset is not None:
                        assert verify(X, target, warm_subset)
                    label = "A solve" if experiment == "A" else (
                        "B reconstruct" if reconstruct else "B count only")
                    for repeat in range(REPEATS):
                        before = time.perf_counter()
                        subset, actual_count = solve(X, target, reconstruct)
                        elapsed = time.perf_counter() - before
                        assert actual_count == count
                        if subset is not None:
                            assert verify(X, target, subset)
                        rows.append({
                            **common, "series": label, "reconstruct": int(reconstruct),
                            "repeat": repeat, "calls": 1, "seconds": elapsed,
                            "solved": int(count is not None), "cardinality": count,
                        })
                if experiment == "B":
                    assert expected_count == 2 and verify(X, target, witness)
                    methods = [
                        ("C solve (successful)", solve, (X, target, True)),
                        ("C pair", solve_pair, (X, target)),
                        ("C hybrid", solve_hybrid, (X, target, True)),
                        ("C verify", verify, (X, target, witness)),
                    ]
                    batches = {label: calibrate(function, args)
                               for label, function, args in methods}
                    for repeat in range(REPEATS):
                        offset = repeat % len(methods)
                        for label, function, args in methods[offset:] + methods[:offset]:
                            result, seconds = time_batch(function, args, batches[label])
                            if label == "C verify":
                                assert result
                            else:
                                subset, count = result
                                assert count == 2 and verify(X, target, subset)
                            rows.append({
                                **common, "experiment": "C", "series": label,
                                "dp_updates": common["dp_updates"] if function is solve else 0,
                                "reconstruct": int(function is not verify), "repeat": repeat,
                                "calls": batches[label], "seconds": seconds,
                                "solved": 1, "cardinality": 2,
                            })
            print(f"{experiment}: n={n}, T={target}, {INSTANCES} instances complete", flush=True)
    assert len(rows) == 1000
    destination = HERE / "results.csv"
    with destination.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print_report(rows)
    elapsed = time.perf_counter() - started
    print(f"Benchmark elapsed: {elapsed:.2f} seconds (300-second budget)")
    if elapsed > 300:
        print("RUNTIME DEVIATION: benchmark exceeded five minutes; all data retained")
    print(f"Wrote {destination}")


if __name__ == "__main__":
    main()
