"""Run the separate all-subset-sizes experiment into a new UTC-stamped folder."""

from collections import Counter, defaultdict
from contextlib import redirect_stdout
import csv
from datetime import datetime, timezone
from importlib.metadata import version
import io
from pathlib import Path
import platform
import random
import statistics
import time

import numpy as np

from benchmark import MAX_CALLS, REPEATS, calibrate, fit_power, time_batch
from subset_sum_all_sizes import solve, solve_hybrid, verify

HERE = Path(__file__).resolve().parent
SIZES = (100, 250, 500, 1000, 2000, 4000)
GROUPS = ("singleton", "pair", "triple", "no_solution")
METHODS = ("DP", "Hybrid", "Verify")


def make_input(group, n, seed):
    """Replay an original input or construct a case with a known optimum."""
    rng = random.Random(seed)
    target = n - 1
    if group in ("singleton", "pair"):
        return sorted(rng.sample(range(1, 3 * n + 1), n))
    if group == "triple":
        planted = {1, 3, target - 4}
        pool = [value for value in range(1, 6 * n + 1, 2)
                if value not in planted and value != target]
        return sorted([*planted, *rng.sample(pool, n - 3)])
    if group == "no_solution":
        return sorted(rng.sample(range(2, 6 * n + 1, 2), n))
    raise ValueError(f"Unknown group: {group}")


def check_case(case, X):
    """Establish the expected answer independently of the measured solvers."""
    n, target, group = case["n"], case["T"], case["group"]
    assert len(X) == n and X == sorted(set(X)) and X[0] > 0
    assert target == n - 1 and target % 2 == 1
    members = set(X)
    if group == "singleton":
        assert target in members and case["expected_cardinality"] == 1
    elif group == "pair":
        assert target not in members and case["expected_cardinality"] == 2
        assert any(target - x in members and target - x != x for x in X)
    elif group == "triple":
        assert target not in members and case["expected_cardinality"] == 3
        assert all(x % 2 == 1 for x in X)
        assert {1, 3, target - 4}.issubset(members)
        assert 1 + 3 + (target - 4) == target
    else:
        assert group == "no_solution" and case["expected_cardinality"] is None
        assert all(x % 2 == 0 for x in X)


def make_cases():
    with (HERE / "results.csv").open(newline="") as source:
        originals = {(int(row["n"]), int(row["instance"])): row
                     for row in csv.DictReader(source) if row["series"] == "C pair"}
    assert set(originals) == {(n, i) for n in SIZES for i in range(5)}
    cases = []
    for (n, instance), row in sorted(originals.items()):
        seed = int(row["instance_seed"])
        assert int(row["T"]) == n - 1 and int(row["master_seed"]) == 20261025
        X = make_input("pair", n, seed)
        count = 1 if n - 1 in X else 2
        cases.append({"group": "singleton" if count == 1 else "pair", "n": n,
                      "T": n - 1, "instance": instance, "master_seed": 20261025,
                      "instance_seed": seed, "expected_cardinality": count})
    for group, master_seed, count in (("triple", 20261026, 3), ("no_solution", 20261027, None)):
        rng = random.Random(master_seed)
        for n in SIZES:
            for instance in range(5):
                cases.append({"group": group, "n": n, "T": n - 1, "instance": instance,
                              "master_seed": master_seed, "instance_seed": rng.getrandbits(64),
                              "expected_cardinality": count})
    assert Counter(case["group"] for case in cases) == {
        "singleton": 8, "pair": 22, "triple": 30, "no_solution": 30}
    for case in cases:
        check_case(case, make_input(case["group"], case["n"], case["instance_seed"]))
    return cases


def summarize(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["group"], row["series"], int(row["n"]), int(row["instance"])].append(
            float(row["seconds"]))
    summaries = {}
    for group in GROUPS:
        summaries[group] = {}
        for method in METHODS:
            points = [(n, statistics.median(times))
                      for (g, label, n, _), times in grouped.items() if (g, label) == (group, method)]
            sizes = sorted({n for n, _ in points})
            medians = [statistics.median(t for n, t in points if n == size) for size in sizes]
            slope, coefficient = fit_power(sizes, medians) if len(sizes) >= 2 else (None, None)
            summaries[group][method] = {"sizes": sizes, "seconds": medians, "points": points,
                                        "slope": slope, "coefficient": coefficient}
    return summaries


def validate_results(rows, cases):
    """Validate both freshly measured and CSV-loaded records before reporting."""
    expected = {(case["group"], case["n"], case["instance"]): case for case in cases}
    assert len(rows) == 1200
    grouped = defaultdict(list)
    for row in rows:
        key = row["group"], int(row["n"]), int(row["instance"])
        case = expected[key]
        for field in ("T", "master_seed", "instance_seed"):
            assert int(row[field]) == case[field]
        count = case["expected_cardinality"]
        for field in ("expected_cardinality", "cardinality"):
            assert row[field] in (None, "") if count is None else int(row[field]) == count
        assert int(row["solved"]) == int(count is not None)
        assert row["series"] in (METHODS if count is not None else METHODS[:2])
        seconds, calls = float(row["seconds"]), int(row["calls"])
        assert np.isfinite(seconds) and seconds > 0
        assert 1 <= calls <= MAX_CALLS and calls & (calls - 1) == 0
        grouped[*key, row["series"]].append(row)
    for key, case in expected.items():
        for method in METHODS if case["expected_cardinality"] is not None else METHODS[:2]:
            measurements = grouped[*key, method]
            assert sorted(int(row["repeat"]) for row in measurements) == list(range(REPEATS))
            assert len({int(row["calls"]) for row in measurements}) == 1


def plot_results(summaries, destination):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {"DP": "#b35806", "Hybrid": "#762a83", "Verify": "#1b7837"}
    figure, axes = plt.subplots(2, 2, figsize=(11, 8), layout="constrained")
    for group, axis in zip(GROUPS, axes.flat):
        for method in METHODS:
            summary = summaries[group][method]
            if not summary["sizes"]:
                continue
            xs, ys = zip(*summary["points"])
            axis.scatter(xs, ys, color=colors[method], alpha=0.3, s=15)
            axis.plot(summary["sizes"], summary["seconds"], "o", color=colors[method], markersize=5)
            sizes = np.array(summary["sizes"])
            axis.plot(sizes, summary["coefficient"] * sizes ** summary["slope"], "--",
                      color=colors[method], label=f"{method}: p={summary['slope']:.3f}")
        title = {"singleton": "Singleton optimum (8 inputs; sparse)",
                 "pair": "Pair optimum (22 inputs)", "triple": "Triple optimum (30 controlled inputs)",
                 "no_solution": "No solution (30 controlled inputs)"}[group]
        axis.set(xscale="log", yscale="log", xlabel="Input size n", ylabel="Seconds per call", title=title)
        axis.grid(True, which="both", alpha=0.18)
        axis.legend(fontsize=9)
        if group == "singleton":
            axis.text(0.98, 0.03, "No singleton input at n=4000", transform=axis.transAxes,
                      ha="right", fontsize=9)
        if group == "no_solution":
            axis.text(0.98, 0.03, "No verification timing: no certificate", transform=axis.transAxes,
                      ha="right", fontsize=9)
    figure.savefig(destination, dpi=200, facecolor="white")
    plt.close(figure)


def write_report(rows, cases, summaries, destination, elapsed, limitations):
    counts = Counter((case["group"], case["n"]) for case in cases)
    metadata = rows[0]
    lines = ["# All subset sizes: separate C rerun", "",
             f"Run: `{metadata['run_id']}` (UTC). **90 inputs, {len(rows)} timing records.**",
             f"Elapsed through validation, CSV writing, and plotting: **{elapsed:.2f} seconds**.", "",
             "All subset sizes are allowed, including empty and full subsets. Inputs remain sorted, "
             "distinct, and strictly positive. Target zero has optimum zero; negative targets have no solution. "
             "Every timed input uses **T=n−1**; unrestricted-target performance is not tested.", "",
             "The hybrid checks zero, then a singleton, then a pair, then DP. Only after excluding smaller "
             "answers does a singleton or pair establish optimality. The early paths validate once; "
             "DP fallback validates again. The verifier checks feasibility, not general optimality.", "",
             "The original 30 C inputs are replayed from saved seeds: 8 now have singleton optima and 22 "
             "have pair optima. Thirty triple inputs contain {1,3,T−4}, exclude T, and contain only odd "
             "values: the odd target cannot be reached by a pair. Thirty impossible inputs contain only "
             "even values against an odd target. New master seeds are 20261026 and 20261027. "
             "These constructed cases exercise fallback; they are not evidence about hard instances. "
             "In particular, a separate parity check could reject the impossible group in linear time.", "",
             f"Environment: Python {metadata['python']}; NumPy {metadata['numpy']}; "
             f"Matplotlib {metadata['matplotlib']}; {metadata['platform']}.", "",
             "Each method receives a warm-up, then calibration by doubling batch size to at least 20 ms "
             "(cap 65,536 calls). Five measured batches retain that call count, with method order rotated "
             "between repeats. Timings include public API validation, result construction, and loop overhead. "
             "Input construction, correctness checks, calibration, and output writing are outside timed batches. "
             "Verification checks the DP certificate and rebuilds membership sets on each call. "
             "No verifier call is timed for an impossible input.", "",
             "Calibration limitations: " + ("; ".join(limitations) if limitations else "none; no cap reached."), "",
             "Times are median repeats per input, then median inputs per size. Ratios divide unrounded "
             "size medians. A ratio above 1 means the numerator took longer. Exponents fit log(time) "
             "against log(n), with equal weight per observed size. They describe this run, not proofs "
             "of asymptotic complexity. Missing sizes are shown as — and never interpolated.", ""]
    for group in GROUPS:
        lines += [f"## {group.replace('_', ' ').capitalize()}", ""]
        if group in ("singleton", "pair"):
            lines += ["Input counts vary by size; these are subsets of the original sample. "
                      "Fits are exploratory, especially the sparse singleton group.", ""]
        lines += ["| Method | Fitted p | Observed sizes |", "| --- | ---: | ---: |"]
        values = {}
        for method in METHODS:
            summary = summaries[group][method]
            slope = summary["slope"]
            fitted = f"{slope:.3f}" if slope is not None else "—"
            lines.append(f"| {method} | {fitted} | {len(summary['sizes'])} |")
            values[method] = dict(zip(summary["sizes"], summary["seconds"]))
        lines += ["", "Times in milliseconds per call:", "",
                  "| n | Inputs | DP | Hybrid | Verify | DP / hybrid | DP / verify | Hybrid / verify |",
                  "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
        for n in SIZES:
            if not counts[group, n]:
                lines.append(f"| {n} | 0 | — | — | — | — | — | — |")
                continue
            dp, hybrid = values["DP"][n], values["Hybrid"][n]
            verification = values["Verify"].get(n)
            verify_time = f"{verification * 1000:.6f}" if verification is not None else "—"
            dp_ratio = f"{dp / verification:.3f}" if verification is not None else "—"
            hybrid_ratio = f"{hybrid / verification:.3f}" if verification is not None else "—"
            lines.append(f"| {n} | {counts[group, n]} | {dp * 1000:.6f} | {hybrid * 1000:.6f} | "
                         f"{verify_time} | {dp / hybrid:.3f} | {dp_ratio} | {hybrid_ratio} |")
        lines.append("")
    lines += ["## Interpretation", "",
              "Singleton and pair paths have linear operation bounds under unit-cost arithmetic. "
              "Fallback retains O(nT) time and reconstruction storage proportional to the retained item "
              "count times T. With T=n−1 this is a quadratic upper bound; it does not require measured "
              "time to grow quadratically over these sizes. Extra checks and repeated validation can "
              "make the hybrid slower on fallback inputs. No speedup threshold is used for acceptance.", "",
              "![Separate timing fits for singleton, pair, triple, and impossible inputs](benchmark.png)", "",
              "[Raw timing records](results.csv). Faint points are input medians, solid points are size "
              "medians, and dashed lines fit observed sizes only. The original experiment and its "
              "documents are unchanged; its timings are not mixed into these ratios.", "",
              "## Reproduce", "", "From the repository root:", "", "```sh",
              ".venv/bin/python -m pytest -q experiments/subset_sum",
              ".venv/bin/python experiments/subset_sum/benchmark_all_sizes.py", "```", "",
              "Each run creates a new UTC-stamped directory and never overwrites a previous run. "
              "With restricted cache access, prefix the benchmark command with "
              "`MPLCONFIGDIR=/tmp/epistemia-mpl-cache XDG_CACHE_HOME=/tmp/epistemia-cache`. "
              "Main README, paper, site, and publication updates remain deferred.", ""]
    with destination.open("x") as output:
        output.write("\n".join(lines))


def main():
    started = time.perf_counter()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    destination = HERE / "all_sizes" / run_id
    destination.mkdir(parents=True, exist_ok=False)
    cases = make_cases()
    metadata = {"run_id": run_id, "python": platform.python_version(), "numpy": np.__version__,
                "matplotlib": version("matplotlib"), "platform": platform.platform(),
                "machine": platform.machine(), "processor": platform.processor()}
    rows, limitations = [], []
    for index, case in enumerate(cases):
        X = make_input(case["group"], case["n"], case["instance_seed"])
        target, expected = case["T"], case["expected_cardinality"]
        witness, count = solve(X, target)
        assert count == expected
        if expected is not None:
            assert witness is not None and len(witness) == expected and verify(X, target, witness)
        else:
            assert witness is None
        methods = [("DP", solve, (X, target, True)), ("Hybrid", solve_hybrid, (X, target, True))]
        if expected is not None:
            methods.append(("Verify", verify, (X, target, witness)))
        batches = {}
        for label, function, args in methods:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                batches[label] = calibrate(function, args)
            if buffer.getvalue():
                message = f"{case['group']} instance {case['instance']}: {buffer.getvalue().strip()}"
                limitations.append(message)
                print(message, flush=True)
        for repeat in range(REPEATS):
            offset = repeat % len(methods)
            for label, function, args in methods[offset:] + methods[:offset]:
                result, seconds = time_batch(function, args, batches[label])
                if label == "Verify":
                    assert result
                else:
                    subset, count = result
                    assert count == expected
                    if expected is None:
                        assert subset is None
                    else:
                        assert len(subset) == expected and verify(X, target, subset)
                rows.append({**metadata, **case, "series": label, "repeat": repeat,
                             "calls": batches[label], "seconds": seconds,
                             "solved": int(expected is not None), "cardinality": expected})
        if (index + 1) % 5 == 0:
            print(f"{index + 1}/90 inputs measured", flush=True)
    validate_results(rows, cases)
    with (destination / "results.csv").open("x", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (destination / "results.csv").open(newline="") as source:
        saved = list(csv.DictReader(source))
    validate_results(saved, cases)
    summaries = summarize(saved)
    plot_results(summaries, destination / "benchmark.png")
    elapsed = time.perf_counter() - started
    write_report(saved, cases, summaries, destination / "REPORT.md", elapsed, limitations)
    print(f"Saved {len(rows)} records in {elapsed:.2f} seconds: {destination}", flush=True)


if __name__ == "__main__":
    main()
