# Incremental partial sums: count-only performance

Run `20261025T183727.014949Z` (UTC): **120 inputs, 2400 timing rows, 480 jobs**.
Statuses: {'COMPLETE': 480}. Total runtime through plotting: **129.86 seconds**.

All four APIs return only the minimum count or NO. DPCount uses solve(reconstruct=False); AscendingCount uses solve_cardinality(reconstruct=False); FibonacciPhasesCount uses solve_fibonacci_gaps(reconstruct=False); FibonacciLayers uses solve_fibonacci_layers. No certificate construction or verification is timed. Expected answers and DP certificates are checked outside timing. Comparisons use fresh measurements from this run, not earlier reconstruction timings.

The same 120 inputs and seeds are replayed: five per group at n=8,12,16,20. Master seeds 20261028–20261033 correspond to singleton, pair, triple, growing, no_solution, and skipped_optimum. Singleton/pair/triple/no-solution targets are T=3n+1; growing targets are the sum of all positive values, forcing full-set answers. Skipped-optimum inputs use T=5n+4 and values congruent to 1 modulo 5 including a planted four-element solution. Impossible cases contain only even values against an odd target. These are controlled families with known answers; they do not claim difficult instances.

Each method/input job has a 15-second worker deadline covering launch, warm-up, calibration, and five measured batches. Batches double until 20 ms or 65,536 calls. Recorded seconds are batch elapsed time divided by calls, including public validation and count-result construction but excluding launch, calibration, correctness assertions and file writing. Method order rotates between inputs. A timeout is missing data, never NO.

Calibration-cap limitations: 0.
Python 3.11.16; NumPy 2.4.6; Matplotlib 3.11.2; macOS-26.6-arm64-arm-64bit.

Input times are medians of five repeats; size times are medians of input times. Ratios divide medians on matched completed inputs; parentheses give their count. Fits use logarithms of observed size medians. Incomplete groups exclude unfinished jobs and may therefore favor faster instances.

## Singleton

| Method | Fitted p | Sizes | Complete / timeout / error |
| --- | ---: | ---: | --- |
| DPCount | 0.651 | 4 | 20 / 0 / 0 |
| AscendingCount | 0.841 | 4 | 20 / 0 / 0 |
| FibonacciPhasesCount | 0.842 | 4 | 20 / 0 / 0 |
| FibonacciLayers | 0.852 | 4 | 20 / 0 / 0 |

Median milliseconds per call. Ratios greater than one favor Layers.

| n | Optimum | DP | Ascending | Phases | Layers | DP / Layers | Ascending / Layers | Phases / Layers |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 1 | 0.005957 | 0.001755 | 0.001744 | 0.001726 | 3.45084 (5) | 1.01686 (5) | 1.01056 (5) |
| 12 | 1 | 0.008104 | 0.002440 | 0.002454 | 0.002442 | 3.31806 (5) | 0.99889 (5) | 1.00474 (5) |
| 16 | 1 | 0.009519 | 0.003105 | 0.003106 | 0.003111 | 3.05939 (5) | 0.997952 (5) | 0.998217 (5) |
| 20 | 1 | 0.010847 | 0.003805 | 0.003787 | 0.003773 | 2.875 (5) | 1.00842 (5) | 1.00373 (5) |

## Pair

| Method | Fitted p | Sizes | Complete / timeout / error |
| --- | ---: | ---: | --- |
| DPCount | 0.814 | 4 | 20 / 0 / 0 |
| AscendingCount | 0.728 | 4 | 20 / 0 / 0 |
| FibonacciPhasesCount | 0.741 | 4 | 20 / 0 / 0 |
| FibonacciLayers | 0.899 | 4 | 20 / 0 / 0 |

Median milliseconds per call. Ratios greater than one favor Layers.

| n | Optimum | DP | Ascending | Phases | Layers | DP / Layers | Ascending / Layers | Phases / Layers |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 2 | 0.006159 | 0.002195 | 0.002178 | 0.002634 | 2.33792 (5) | 0.833277 (5) | 0.826735 (5) |
| 12 | 2 | 0.007663 | 0.002846 | 0.002845 | 0.003487 | 2.19765 (5) | 0.816242 (5) | 0.815889 (5) |
| 16 | 2 | 0.010113 | 0.003584 | 0.003559 | 0.004909 | 2.06026 (5) | 0.730058 (5) | 0.725018 (5) |
| 20 | 2 | 0.013044 | 0.004271 | 0.004305 | 0.005889 | 2.21508 (5) | 0.725351 (5) | 0.731074 (5) |

## Triple

| Method | Fitted p | Sizes | Complete / timeout / error |
| --- | ---: | ---: | --- |
| DPCount | 0.779 | 4 | 20 / 0 / 0 |
| AscendingCount | 0.697 | 4 | 20 / 0 / 0 |
| FibonacciPhasesCount | 0.665 | 4 | 20 / 0 / 0 |
| FibonacciLayers | 1.017 | 4 | 20 / 0 / 0 |

Median milliseconds per call. Ratios greater than one favor Layers.

| n | Optimum | DP | Ascending | Phases | Layers | DP / Layers | Ascending / Layers | Phases / Layers |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 3 | 0.006184 | 0.002632 | 0.002750 | 0.003683 | 1.67903 (5) | 0.714643 (5) | 0.746675 (5) |
| 12 | 3 | 0.008326 | 0.003470 | 0.003617 | 0.005356 | 1.55455 (5) | 0.64784 (5) | 0.675323 (5) |
| 16 | 3 | 0.010332 | 0.004170 | 0.004295 | 0.006583 | 1.56946 (5) | 0.633401 (5) | 0.652357 (5) |
| 20 | 3 | 0.012727 | 0.005029 | 0.005099 | 0.009807 | 1.29777 (5) | 0.512797 (5) | 0.519952 (5) |

## Growing

| Method | Fitted p | Sizes | Complete / timeout / error |
| --- | ---: | ---: | --- |
| DPCount | 1.075 | 4 | 20 / 0 / 0 |
| AscendingCount | 9.091 | 4 | 20 / 0 / 0 |
| FibonacciPhasesCount | 9.074 | 4 | 20 / 0 / 0 |
| FibonacciLayers | 4.062 | 4 | 20 / 0 / 0 |

Median milliseconds per call. Ratios greater than one favor Layers.

| n | Optimum | DP | Ascending | Phases | Layers | DP / Layers | Ascending / Layers | Phases / Layers |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 8 | 0.008718 | 0.019034 | 0.019357 | 0.017814 | 0.489407 (5) | 1.06846 (5) | 1.0866 (5) |
| 12 | 12 | 0.013018 | 0.284380 | 0.283307 | 0.090135 | 0.14443 (5) | 3.15504 (5) | 3.14314 (5) |
| 16 | 16 | 0.017438 | 4.978026 | 4.967766 | 0.296392 | 0.0588344 (5) | 16.7954 (5) | 16.7608 (5) |
| 20 | 20 | 0.023699 | 87.558041 | 87.675166 | 0.733132 | 0.0323261 (5) | 119.43 (5) | 119.59 (5) |

## No Solution

| Method | Fitted p | Sizes | Complete / timeout / error |
| --- | ---: | ---: | --- |
| DPCount | 0.681 | 4 | 20 / 0 / 0 |
| AscendingCount | 2.901 | 4 | 20 / 0 / 0 |
| FibonacciPhasesCount | 2.853 | 4 | 20 / 0 / 0 |
| FibonacciLayers | 1.168 | 4 | 20 / 0 / 0 |

Median milliseconds per call. Ratios greater than one favor Layers.

| n | Optimum | DP | Ascending | Phases | Layers | DP / Layers | Ascending / Layers | Phases / Layers |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | NO | 0.006117 | 0.004335 | 0.004594 | 0.003050 | 2.00583 (5) | 1.42151 (5) | 1.50636 (5) |
| 12 | NO | 0.008399 | 0.011530 | 0.011709 | 0.006050 | 1.38835 (5) | 1.90587 (5) | 1.93559 (5) |
| 16 | NO | 0.009703 | 0.020753 | 0.020957 | 0.006191 | 1.56715 (5) | 3.35189 (5) | 3.38499 (5) |
| 20 | NO | 0.011590 | 0.072415 | 0.073539 | 0.009797 | 1.18298 (5) | 7.3914 (5) | 7.50618 (5) |

## Skipped Optimum

| Method | Fitted p | Sizes | Complete / timeout / error |
| --- | ---: | ---: | --- |
| DPCount | 0.899 | 4 | 20 / 0 / 0 |
| AscendingCount | 1.108 | 4 | 20 / 0 / 0 |
| FibonacciPhasesCount | 1.072 | 4 | 20 / 0 / 0 |
| FibonacciLayers | 1.344 | 4 | 20 / 0 / 0 |

Median milliseconds per call. Ratios greater than one favor Layers.

| n | Optimum | DP | Ascending | Phases | Layers | DP / Layers | Ascending / Layers | Phases / Layers |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 4 | 0.008462 | 0.004679 | 0.004909 | 0.005281 | 1.60231 (5) | 0.885956 (5) | 0.929558 (5) |
| 12 | 4 | 0.012209 | 0.007153 | 0.007333 | 0.009049 | 1.34922 (5) | 0.790432 (5) | 0.810343 (5) |
| 16 | 4 | 0.015698 | 0.009862 | 0.010047 | 0.013124 | 1.19615 (5) | 0.751423 (5) | 0.76551 (5) |
| 20 | 4 | 0.019330 | 0.012972 | 0.013173 | 0.018237 | 1.05992 (5) | 0.711306 (5) | 0.722308 (5) |

## Interpretation and reproduction

Layers reuse partial sums, retaining the earliest endpoint at each sum and cardinality. The expected O(n²T) time and O(n+T) space bounds are pseudo-polynomial in numeric T. The DP comparator has an O(nT) bound; exact-size searches remain combinatorial. Fibonacci boundaries alone do not reduce work. Fits over four small sizes are descriptions of this run, not asymptotic proofs. Large targets, sizes above 20, and layer reconstruction are not measured. No conclusion about P versus NP follows.

![Count-only comparisons across six groups](benchmark.png)

[Raw times](results.csv) · [Completion and timeout ledger](ledger.csv)

```sh
.venv/bin/python -m pytest -q experiments/subset_sum
MPLCONFIGDIR=/tmp/epistemia-mpl-cache XDG_CACHE_HOME=/tmp/epistemia-cache .venv/bin/python experiments/subset_sum/benchmark_layers.py
```

Each run creates a new timestamped directory; earlier artifacts are preserved.
