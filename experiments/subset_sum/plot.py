"""Render the recorded CSV; no measurements are rerun here."""

import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from benchmark import HERE, print_report, summarize


def main():
    with (HERE / "results.csv").open(newline="") as source:
        rows = list(csv.DictReader(source))
    summaries = summarize(rows)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    figure, axes = plt.subplots(3, 1, figsize=(7, 9), layout="constrained")
    panels = [
        ("A: Unrestricted target, n = 100", "Target T", ["A solve"]),
        ("B: Restricted target T = n − 1", "Input size n", ["B count only", "B reconstruct"]),
        ("C: Pair-containing instances — optimal solving and checking", "Input size n",
         ["C solve (successful)", "C pair", "C hybrid", "C verify"]),
    ]
    colors = {"A solve": "#2166ac", "B count only": "#2166ac", "B reconstruct": "#b35806",
              "C solve (successful)": "#b35806", "C pair": "#2166ac",
              "C hybrid": "#762a83", "C verify": "#1b7837"}
    markers = {"C pair": "s", "C hybrid": "^"}
    styles = {"C pair": ":", "C hybrid": "-."}
    for axis, (title, xlabel, labels) in zip(axes, panels):
        for label in labels:
            summary = summaries[label]
            color = colors[label]
            if summary["points"]:
                xs, ys = zip(*summary["points"])
                axis.scatter(xs, ys, color=color, alpha=0.3, s=16)
            if summary["slope"] is None:
                continue
            sizes = np.asarray(summary["sizes"])
            axis.plot(sizes, summary["seconds"], markers.get(label, "o"),
                      color=color, markersize=5)
            fit = summary["coefficient"] * sizes ** summary["slope"]
            axis.plot(sizes, fit, styles.get(label, "--"), color=color,
                      label=f"{label}: p = {summary['slope']:.2f} (expected {summary['expected']})")
        axis.set(xscale="log", yscale="log", xlabel=xlabel, ylabel="Seconds per call", title=title)
        axis.grid(True, which="both", alpha=0.18)
        axis.legend(fontsize=9, loc="best")
    figure.savefig(HERE / "benchmark.png", dpi=300, facecolor="white")
    plt.close(figure)
    print(f"Wrote {HERE / 'benchmark.png'}")
    print_report(rows)


if __name__ == "__main__":
    main()
