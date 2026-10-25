# Ascending and two Fibonacci cardinality search orders

Run `20261025T174141.150008Z` (UTC): **120 inputs, 3500 timing rows, 700 method/input jobs**.
Statuses: {'COMPLETE': 700}. Elapsed through plotting: **189.49 seconds**.

All three searches fix every combination of k−2 indices and use two pointers on the later suffix to search exactly k elements. Cardinality tries k in ascending order. Fibonacci tries 2,3,5,8,13,… until its first success, then checks every untested smaller size in ascending order. A Fibonacci success is only a candidate until those checks finish. If no Fibonacci size succeeds, it checks every remaining size before returning NO. No size is checked twice. Empty and full subsets are allowed; zero and singleton answers are handled first. FibonacciPhases holds each endpoint while searching its preceding gap ascending, then checks the endpoint only if the gap fails. Its phases are [2], [3], [4,5], [6,7,8], [9,10,11,12,13], and so on. The final partial phase is searched through the retained input count. The actual exact-k call order is 2,3,4,5,6,…, identical to Cardinality. It returns immediately at the first success. This is the revised solve_fibonacci_gaps function; older runs labeled FibonacciGaps measured the earlier endpoint-first order. None of these three searches uses DP fallback or parity shortcuts.

Five inputs per size n=8,12,16,20 in each group. Master seeds 20261028–20261033 correspond to singleton, pair, triple, growing, no-solution, and skipped-optimum groups. All 120 inputs replay the preceding Fibonacci study unchanged. The first 100 inputs replay the earlier seeds unchanged. Singleton, pair, triple, and no-solution targets are T=3n+1, with values sampled from [1,6n]. Singleton inputs contain T; pair inputs exclude T and contain {1,T−1}; triple inputs exclude T and contain only odd values including {1,3,T−4}. Impossible inputs contain only even values against the odd target. Growing inputs sample from [1,3n] and target the sum of all values, so their optimum is n. These constructions establish the expected answers independently. Skipped-optimum inputs use T=5n+4 and n distinct values congruent to 1 modulo 5 from [1,T], including {1,6,11,T−18}. Every solution must have cardinality 4 modulo 5: the planted four-element answer is optimal, and no Fibonacci size tested at n≤20 can work. The impossible family could be rejected cheaply by parity; it is a controlled test, not a hardness claim.

These target families differ from the earlier T=n−1 study. Compare methods within each group; do not mix historical timings into ratios.

Python 3.11.16; NumPy 2.4.6; Matplotlib 3.11.2; macOS-26.6-arm64-arm-64bit.

Every method/input job runs in a spawned worker with a 15-second deadline covering startup, warm-up, calibration, and five repeats. Recorded call times exclude startup and IPC, and include API validation, result construction, and loop overhead. Calibration doubles batches to 20 ms (cap 65,536 calls). Method order rotates between inputs. Correctness checks are outside timed batches. Timed-out jobs contribute no partial times and never count as NO. Verification uses a DP certificate and is not measured for impossible inputs.

Calibration-cap reports: 0.

Each input time is the median of five batch averages. Size times are medians across completed inputs. Ratios use the intersection of completed inputs for the two methods and divide their size medians; parentheses give the matched count. Fits use observed size medians only. Incomplete samples are biased toward jobs that completed, and are explicitly flagged below.

## Singleton

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.661 | 4 | 20 / 0 / 0 |
| Hybrid | 0.794 | 4 | 20 / 0 / 0 |
| Cardinality | 0.851 | 4 | 20 / 0 / 0 |
| Fibonacci | 0.847 | 4 | 20 / 0 / 0 |
| FibonacciPhases | 0.856 | 4 | 20 / 0 / 0 |
| Verify | 0.730 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciPhases (gap before endpoint).

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 1 | 0.010009 | 0.001715 | 0.001751 | 0.001740 | 0.001748 | 0.001921 | 1.00189 (5) | 0.995412 (5) | 5.72695 (5) | 0.98105 (5) | 0.909675 (5) |
| 12 | 1 | 0.013548 | 0.002334 | 0.002424 | 0.002449 | 0.002435 | 0.002509 | 0.995302 (5) | 1.00551 (5) | 5.56317 (5) | 0.958515 (5) | 0.970719 (5) |
| 16 | 1 | 0.016057 | 0.002932 | 0.003149 | 0.003123 | 0.003117 | 0.003089 | 1.01019 (5) | 1.00188 (5) | 5.15128 (5) | 0.940744 (5) | 1.00923 (5) |
| 20 | 1 | 0.018373 | 0.003560 | 0.003808 | 0.003782 | 0.003840 | 0.003777 | 0.991438 (5) | 0.984713 (5) | 4.78411 (5) | 0.927086 (5) | 1.01669 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciPhases | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciPhases | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciPhases | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciPhases | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Pair

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.884 | 4 | 20 / 0 / 0 |
| Hybrid | 0.854 | 4 | 20 / 0 / 0 |
| Cardinality | 0.727 | 4 | 20 / 0 / 0 |
| Fibonacci | 0.723 | 4 | 20 / 0 / 0 |
| FibonacciPhases | 0.729 | 4 | 20 / 0 / 0 |
| Verify | 0.675 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciPhases (gap before endpoint).

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 2 | 0.010346 | 0.002019 | 0.002237 | 0.002288 | 0.002266 | 0.002163 | 0.987292 (5) | 1.00969 (5) | 4.56606 (5) | 0.891044 (5) | 1.04761 (5) |
| 12 | 2 | 0.012507 | 0.002911 | 0.002979 | 0.003014 | 0.003017 | 0.002771 | 0.987458 (5) | 0.999044 (5) | 4.14536 (5) | 0.96498 (5) | 1.08878 (5) |
| 16 | 2 | 0.017881 | 0.003696 | 0.003650 | 0.003741 | 0.003700 | 0.003373 | 0.986415 (5) | 1.01096 (5) | 4.83242 (5) | 0.998891 (5) | 1.09699 (5) |
| 20 | 2 | 0.023030 | 0.004408 | 0.004373 | 0.004437 | 0.004441 | 0.004031 | 0.984759 (5) | 0.999229 (5) | 5.18601 (5) | 0.992571 (5) | 1.10168 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciPhases | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciPhases | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciPhases | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciPhases | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Triple

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.776 | 4 | 20 / 0 / 0 |
| Hybrid | 0.798 | 4 | 20 / 0 / 0 |
| Cardinality | 0.677 | 4 | 20 / 0 / 0 |
| Fibonacci | 0.667 | 4 | 20 / 0 / 0 |
| FibonacciPhases | 0.665 | 4 | 20 / 0 / 0 |
| Verify | 0.649 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciPhases (gap before endpoint).

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 3 | 0.010557 | 0.012867 | 0.002761 | 0.002833 | 0.002842 | 0.002330 | 0.971466 (5) | 0.996945 (5) | 3.71501 (5) | 4.52794 (5) | 1.21946 (5) |
| 12 | 3 | 0.014081 | 0.017417 | 0.003548 | 0.003665 | 0.003666 | 0.002940 | 0.967772 (5) | 0.99976 (5) | 3.841 (5) | 4.75118 (5) | 1.24677 (5) |
| 16 | 3 | 0.017536 | 0.021936 | 0.004303 | 0.004430 | 0.004429 | 0.003529 | 0.971565 (5) | 1.00025 (5) | 3.95943 (5) | 4.95305 (5) | 1.2548 (5) |
| 20 | 3 | 0.021663 | 0.026842 | 0.005162 | 0.005239 | 0.005248 | 0.004258 | 0.983607 (5) | 0.998317 (5) | 4.12781 (5) | 5.11461 (5) | 1.23248 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciPhases | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciPhases | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciPhases | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciPhases | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Growing

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 1.154 | 4 | 20 / 0 / 0 |
| Hybrid | 1.128 | 4 | 20 / 0 / 0 |
| Cardinality | 9.076 | 4 | 20 / 0 / 0 |
| Fibonacci | 9.065 | 4 | 20 / 0 / 0 |
| FibonacciPhases | 9.063 | 4 | 20 / 0 / 0 |
| Verify | 0.890 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciPhases (gap before endpoint).

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 8 | 0.015413 | 0.017715 | 0.019557 | 0.019576 | 0.019694 | 0.003282 | 0.99307 (5) | 0.994047 (5) | 0.782621 (5) | 0.899515 (5) | 6.00125 (5) |
| 12 | 12 | 0.024022 | 0.027697 | 0.285531 | 0.285954 | 0.286244 | 0.004649 | 0.997506 (5) | 0.998984 (5) | 0.0839225 (5) | 0.0967593 (5) | 61.572 (5) |
| 16 | 16 | 0.032985 | 0.036972 | 4.995234 | 4.984474 | 4.987214 | 0.005958 | 1.00161 (5) | 0.999451 (5) | 0.00661393 (5) | 0.00741336 (5) | 837.111 (5) |
| 20 | 20 | 0.044894 | 0.050756 | 88.932542 | 88.049958 | 88.421917 | 0.007466 | 1.00577 (5) | 0.995793 (5) | 0.000507725 (5) | 0.000574025 (5) | 11843.3 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciPhases | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciPhases | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciPhases | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciPhases | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## No Solution

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.683 | 4 | 20 / 0 / 0 |
| Hybrid | 0.721 | 4 | 20 / 0 / 0 |
| Cardinality | 2.906 | 4 | 20 / 0 / 0 |
| Fibonacci | 2.874 | 4 | 20 / 0 / 0 |
| FibonacciPhases | 2.851 | 4 | 20 / 0 / 0 |
| Verify | — | 0 | 0 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciPhases (gap before endpoint).

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | NO | 0.010190 | 0.012602 | 0.004388 | 0.004466 | 0.004585 | — | 0.956959 (5) | 0.974004 (5) | 2.22253 (5) | 2.74866 (5) | — (0) |
| 12 | NO | 0.013760 | 0.017092 | 0.011550 | 0.011585 | 0.011809 | — | 0.978058 (5) | 0.980975 (5) | 1.16518 (5) | 1.44732 (5) | — (0) |
| 16 | NO | 0.016061 | 0.020462 | 0.021040 | 0.021024 | 0.021092 | — | 0.997506 (5) | 0.996778 (5) | 0.761454 (5) | 0.970102 (5) | — (0) |
| 20 | NO | 0.019333 | 0.024651 | 0.073451 | 0.072410 | 0.073055 | — | 1.00542 (5) | 0.991183 (5) | 0.264637 (5) | 0.337436 (5) | — (0) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciPhases | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciPhases | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciPhases | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciPhases | 5 | 0 | 0 |

## Skipped Optimum

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.926 | 4 | 20 / 0 / 0 |
| Hybrid | 0.927 | 4 | 20 / 0 / 0 |
| Cardinality | 1.100 | 4 | 20 / 0 / 0 |
| Fibonacci | 7.933 | 4 | 20 / 0 / 0 |
| FibonacciPhases | 1.074 | 4 | 20 / 0 / 0 |
| Verify | 0.600 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciPhases (gap before endpoint).

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 4 | 0.015264 | 0.017756 | 0.004827 | 0.010544 | 0.005023 | 0.002549 | 0.960983 (5) | 2.09902 (5) | 3.03868 (5) | 3.5348 (5) | 1.97082 (5) |
| 12 | 4 | 0.021762 | 0.025113 | 0.007303 | 0.098931 | 0.007472 | 0.003154 | 0.977448 (5) | 13.2405 (5) | 2.91247 (5) | 3.36099 (5) | 2.36896 (5) |
| 16 | 4 | 0.028888 | 0.033349 | 0.010265 | 1.143404 | 0.010400 | 0.003771 | 0.987022 (5) | 109.945 (5) | 2.77776 (5) | 3.20667 (5) | 2.75773 (5) |
| 20 | 4 | 0.035528 | 0.041445 | 0.013173 | 17.413605 | 0.013417 | 0.004433 | 0.981763 (5) | 1297.83 (5) | 2.64789 (5) | 3.08887 (5) | 3.02657 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciPhases | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciPhases | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciPhases | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciPhases | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Limits and reproduction

For fixed k, the straightforward search bound is O(n^(k−1)). Searching all sizes has combinatorial worst-case cost. A power-law fit over four sizes does not turn that into a polynomial guarantee. Original Fibonacci-first ordering may add searches above the minimum. FibonacciPhases performs the same exact-k searches as ascending search; its phase boundaries do not reduce the work. Small-target DP also has favorable table sizes here. No conclusion about P versus NP follows.

![Timing comparisons by group](benchmark.png)

[Raw times](results.csv) · [Completion and timeout ledger](ledger.csv). Faint points are input medians; opaque markers are size medians; dashed lines fit completed observations.

```sh
.venv/bin/python -m pytest -q experiments/subset_sum
.venv/bin/python experiments/subset_sum/benchmark_cardinality.py
```

Each run creates a fresh UTC-stamped directory. Earlier run artifacts remain unchanged. The benchmark does not update the README, paper, site, or publication. With restricted cache access, prefix the benchmark command with `MPLCONFIGDIR=/tmp/epistemia-mpl-cache XDG_CACHE_HOME=/tmp/epistemia-cache`.
