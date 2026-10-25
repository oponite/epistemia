# Ascending and two Fibonacci cardinality search orders

Run `20261025T164729.762497Z` (UTC): **120 inputs, 3500 timing rows, 700 method/input jobs**.
Statuses: {'COMPLETE': 700}. Elapsed through plotting: **189.46 seconds**.

All three searches fix every combination of k−2 indices and use two pointers on the later suffix to search exactly k elements. Cardinality tries k in ascending order. Fibonacci tries 2,3,5,8,13,… until its first success, then checks every untested smaller size in ascending order. A Fibonacci success is only a candidate until those checks finish. If no Fibonacci size succeeds, it checks every remaining size before returning NO. No size is checked twice. Empty and full subsets are allowed; zero and singleton answers are handled first. FibonacciGaps checks each endpoint, then immediately fills its preceding gap ascending before advancing. A gap success takes priority over a saved endpoint success. Remaining sizes after the last eligible endpoint are checked ascending before NO. Thus its order is 2,3,5,4,8,6,7,13,9,10,11,12,… when checks fail. All smaller sizes have failed before any answer is returned. None of these three searches uses DP fallback or parity shortcuts.

Five inputs per size n=8,12,16,20 in each group. Master seeds 20261028–20261033 correspond to singleton, pair, triple, growing, no-solution, and skipped-optimum groups. All 120 inputs replay the preceding Fibonacci study unchanged. The first 100 inputs replay the earlier seeds unchanged. Singleton, pair, triple, and no-solution targets are T=3n+1, with values sampled from [1,6n]. Singleton inputs contain T; pair inputs exclude T and contain {1,T−1}; triple inputs exclude T and contain only odd values including {1,3,T−4}. Impossible inputs contain only even values against the odd target. Growing inputs sample from [1,3n] and target the sum of all values, so their optimum is n. These constructions establish the expected answers independently. Skipped-optimum inputs use T=5n+4 and n distinct values congruent to 1 modulo 5 from [1,T], including {1,6,11,T−18}. Every solution must have cardinality 4 modulo 5: the planted four-element answer is optimal, and no Fibonacci size tested at n≤20 can work. The impossible family could be rejected cheaply by parity; it is a controlled test, not a hardness claim.

These target families differ from the earlier T=n−1 study. Compare methods within each group; do not mix historical timings into ratios.

Python 3.11.16; NumPy 2.4.6; Matplotlib 3.11.2; macOS-26.6-arm64-arm-64bit.

Every method/input job runs in a spawned worker with a 15-second deadline covering startup, warm-up, calibration, and five repeats. Recorded call times exclude startup and IPC, and include API validation, result construction, and loop overhead. Calibration doubles batches to 20 ms (cap 65,536 calls). Method order rotates between inputs. Correctness checks are outside timed batches. Timed-out jobs contribute no partial times and never count as NO. Verification uses a DP certificate and is not measured for impossible inputs.

Calibration-cap reports: 0.

Each input time is the median of five batch averages. Size times are medians across completed inputs. Ratios use the intersection of completed inputs for the two methods and divide their size medians; parentheses give the matched count. Fits use observed size medians only. Incomplete samples are biased toward jobs that completed, and are explicitly flagged below.

## Singleton

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.656 | 4 | 20 / 0 / 0 |
| Hybrid | 0.828 | 4 | 20 / 0 / 0 |
| Cardinality | 0.859 | 4 | 20 / 0 / 0 |
| Fibonacci | 0.851 | 4 | 20 / 0 / 0 |
| FibonacciGaps | 0.856 | 4 | 20 / 0 / 0 |
| Verify | 0.746 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciGaps.

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 1 | 0.009980 | 0.001680 | 0.001726 | 0.001737 | 0.001750 | 0.001917 | 0.985875 (5) | 0.992248 (5) | 5.70183 (5) | 0.960151 (5) | 0.913029 (5) |
| 12 | 1 | 0.013517 | 0.002316 | 0.002458 | 0.002439 | 0.002429 | 0.002482 | 1.01206 (5) | 1.00409 (5) | 5.56535 (5) | 0.953411 (5) | 0.978556 (5) |
| 16 | 1 | 0.015954 | 0.002946 | 0.003098 | 0.003126 | 0.003149 | 0.003094 | 0.983744 (5) | 0.992609 (5) | 5.06642 (5) | 0.935618 (5) | 1.01778 (5) |
| 20 | 1 | 0.018243 | 0.003595 | 0.003814 | 0.003784 | 0.003827 | 0.003825 | 0.996526 (5) | 0.988759 (5) | 4.76647 (5) | 0.939202 (5) | 1.00054 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciGaps | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciGaps | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciGaps | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciGaps | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Pair

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.866 | 4 | 20 / 0 / 0 |
| Hybrid | 0.844 | 4 | 20 / 0 / 0 |
| Cardinality | 0.737 | 4 | 20 / 0 / 0 |
| Fibonacci | 0.726 | 4 | 20 / 0 / 0 |
| FibonacciGaps | 0.723 | 4 | 20 / 0 / 0 |
| Verify | 0.673 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciGaps.

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 2 | 0.010366 | 0.002019 | 0.002224 | 0.002267 | 0.002238 | 0.002135 | 0.993862 (5) | 1.01313 (5) | 4.63204 (5) | 0.902024 (5) | 1.04828 (5) |
| 12 | 2 | 0.012365 | 0.002857 | 0.002913 | 0.002977 | 0.002933 | 0.002738 | 0.993036 (5) | 1.01483 (5) | 4.21544 (5) | 0.974085 (5) | 1.07129 (5) |
| 16 | 2 | 0.017645 | 0.003629 | 0.003655 | 0.003666 | 0.003635 | 0.003317 | 1.0054 (5) | 1.00833 (5) | 4.85373 (5) | 0.998376 (5) | 1.09592 (5) |
| 20 | 2 | 0.022678 | 0.004379 | 0.004367 | 0.004435 | 0.004351 | 0.003979 | 1.00382 (5) | 1.01932 (5) | 5.2124 (5) | 1.0064 (5) | 1.09344 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciGaps | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciGaps | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciGaps | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciGaps | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Triple

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.783 | 4 | 20 / 0 / 0 |
| Hybrid | 0.790 | 4 | 20 / 0 / 0 |
| Cardinality | 0.660 | 4 | 20 / 0 / 0 |
| Fibonacci | 0.648 | 4 | 20 / 0 / 0 |
| FibonacciGaps | 0.652 | 4 | 20 / 0 / 0 |
| Verify | 0.623 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciGaps.

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 3 | 0.010362 | 0.012757 | 0.002760 | 0.002868 | 0.002800 | 0.002355 | 0.985441 (5) | 1.02402 (5) | 3.7 (5) | 4.55538 (5) | 1.18892 (5) |
| 12 | 3 | 0.014298 | 0.017408 | 0.003513 | 0.003676 | 0.003595 | 0.002976 | 0.977143 (5) | 1.02263 (5) | 3.9776 (5) | 4.84253 (5) | 1.20777 (5) |
| 16 | 3 | 0.017534 | 0.021680 | 0.004255 | 0.004403 | 0.004311 | 0.003512 | 0.986994 (5) | 1.02137 (5) | 4.06753 (5) | 5.0294 (5) | 1.2274 (5) |
| 20 | 3 | 0.021430 | 0.026465 | 0.005078 | 0.005225 | 0.005117 | 0.004212 | 0.992186 (5) | 1.02101 (5) | 4.18754 (5) | 5.17146 (5) | 1.21498 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciGaps | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciGaps | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciGaps | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciGaps | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Growing

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 1.144 | 4 | 20 / 0 / 0 |
| Hybrid | 1.123 | 4 | 20 / 0 / 0 |
| Cardinality | 9.082 | 4 | 20 / 0 / 0 |
| Fibonacci | 9.060 | 4 | 20 / 0 / 0 |
| FibonacciGaps | 9.060 | 4 | 20 / 0 / 0 |
| Verify | 0.890 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciGaps.

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 8 | 0.015304 | 0.017529 | 0.019295 | 0.019496 | 0.019625 | 0.003286 | 0.983166 (5) | 0.993422 (5) | 0.779806 (5) | 0.89317 (5) | 5.97162 (5) |
| 12 | 12 | 0.023488 | 0.027129 | 0.284391 | 0.283307 | 0.286165 | 0.004577 | 0.993799 (5) | 0.99001 (5) | 0.082077 (5) | 0.0948008 (5) | 62.5206 (5) |
| 16 | 16 | 0.032521 | 0.036395 | 4.971672 | 4.934125 | 4.965104 | 0.005933 | 1.00132 (5) | 0.993761 (5) | 0.00654985 (5) | 0.00733022 (5) | 836.888 (5) |
| 20 | 20 | 0.044065 | 0.049897 | 88.093458 | 87.235583 | 87.929375 | 0.007463 | 1.00187 (5) | 0.99211 (5) | 0.000501146 (5) | 0.000567464 (5) | 11781.6 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciGaps | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciGaps | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciGaps | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciGaps | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## No Solution

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.715 | 4 | 20 / 0 / 0 |
| Hybrid | 0.731 | 4 | 20 / 0 / 0 |
| Cardinality | 2.913 | 4 | 20 / 0 / 0 |
| Fibonacci | 2.870 | 4 | 20 / 0 / 0 |
| FibonacciGaps | 2.845 | 4 | 20 / 0 / 0 |
| Verify | — | 0 | 0 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciGaps.

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | NO | 0.009951 | 0.012412 | 0.004329 | 0.004486 | 0.004598 | — | 0.941558 (5) | 0.975627 (5) | 2.16442 (5) | 2.69974 (5) | — (0) |
| 12 | NO | 0.013311 | 0.017190 | 0.011479 | 0.011543 | 0.011731 | — | 0.97857 (5) | 0.984037 (5) | 1.13469 (5) | 1.46544 (5) | — (0) |
| 16 | NO | 0.015801 | 0.020265 | 0.020895 | 0.020775 | 0.021046 | — | 0.992794 (5) | 0.987122 (5) | 0.750764 (5) | 0.962901 (5) | — (0) |
| 20 | NO | 0.019468 | 0.024603 | 0.072945 | 0.072801 | 0.072800 | — | 1.00198 (5) | 1.00001 (5) | 0.267419 (5) | 0.337945 (5) | — (0) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciGaps | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciGaps | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciGaps | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciGaps | 5 | 0 | 0 |

## Skipped Optimum

| Method | Fitted p | Sizes | Completed / timed out / error |
| --- | ---: | ---: | --- |
| DP | 0.949 | 4 | 20 / 0 / 0 |
| Hybrid | 0.940 | 4 | 20 / 0 / 0 |
| Cardinality | 1.102 | 4 | 20 / 0 / 0 |
| Fibonacci | 7.946 | 4 | 20 / 0 / 0 |
| FibonacciGaps | 3.572 | 4 | 20 / 0 / 0 |
| Verify | 0.598 | 4 | 20 / 0 / 0 |

Times in milliseconds; A denotes ascending Cardinality search, F denotes original Fibonacci-first search, and G denotes FibonacciGaps.

| n | Optimum | DP | Hybrid | A | F | G | Verify | A / G (matched) | F / G (matched) | DP / G (matched) | Hybrid / G (matched) | G / Verify (matched) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 4 | 0.014984 | 0.017305 | 0.004781 | 0.010392 | 0.009994 | 0.002533 | 0.478429 (5) | 1.03985 (5) | 1.49929 (5) | 1.73147 (5) | 3.94596 (5) |
| 12 | 4 | 0.021976 | 0.025370 | 0.007371 | 0.099258 | 0.039796 | 0.003152 | 0.185219 (5) | 2.49418 (5) | 0.552218 (5) | 0.637511 (5) | 12.6243 (5) |
| 16 | 4 | 0.028450 | 0.033112 | 0.010100 | 1.123721 | 0.114854 | 0.003722 | 0.0879402 (5) | 9.78395 (5) | 0.247704 (5) | 0.288298 (5) | 30.8608 (5) |
| 20 | 4 | 0.035994 | 0.040989 | 0.013175 | 17.507479 | 0.263732 | 0.004415 | 0.0499543 (5) | 66.3836 (5) | 0.13648 (5) | 0.155419 (5) | 59.7411 (5) |

| n | Method | Completed | Timed out | Error |
| ---: | --- | ---: | ---: | ---: |
| 8 | DP | 5 | 0 | 0 |
| 8 | Hybrid | 5 | 0 | 0 |
| 8 | Cardinality | 5 | 0 | 0 |
| 8 | Fibonacci | 5 | 0 | 0 |
| 8 | FibonacciGaps | 5 | 0 | 0 |
| 8 | Verify | 5 | 0 | 0 |
| 12 | DP | 5 | 0 | 0 |
| 12 | Hybrid | 5 | 0 | 0 |
| 12 | Cardinality | 5 | 0 | 0 |
| 12 | Fibonacci | 5 | 0 | 0 |
| 12 | FibonacciGaps | 5 | 0 | 0 |
| 12 | Verify | 5 | 0 | 0 |
| 16 | DP | 5 | 0 | 0 |
| 16 | Hybrid | 5 | 0 | 0 |
| 16 | Cardinality | 5 | 0 | 0 |
| 16 | Fibonacci | 5 | 0 | 0 |
| 16 | FibonacciGaps | 5 | 0 | 0 |
| 16 | Verify | 5 | 0 | 0 |
| 20 | DP | 5 | 0 | 0 |
| 20 | Hybrid | 5 | 0 | 0 |
| 20 | Cardinality | 5 | 0 | 0 |
| 20 | Fibonacci | 5 | 0 | 0 |
| 20 | FibonacciGaps | 5 | 0 | 0 |
| 20 | Verify | 5 | 0 | 0 |

## Limits and reproduction

For fixed k, the straightforward search bound is O(n^(k−1)). Searching all sizes has combinatorial worst-case cost. A power-law fit over four sizes does not turn that into a polynomial guarantee. Fibonacci ordering still performs every exact-size search needed by ascending search to certify the minimum, and may add searches above it; this is particularly important for the growing-optimum group. Small-target DP also has favorable table sizes here. No conclusion about P versus NP follows.

![Timing comparisons by group](benchmark.png)

[Raw times](results.csv) · [Completion and timeout ledger](ledger.csv). Faint points are input medians; opaque markers are size medians; dashed lines fit completed observations.

```sh
.venv/bin/python -m pytest -q experiments/subset_sum
.venv/bin/python experiments/subset_sum/benchmark_cardinality.py
```

Each run creates a fresh UTC-stamped directory. Earlier run artifacts remain unchanged. The benchmark does not update the README, paper, site, or publication. With restricted cache access, prefix the benchmark command with `MPLCONFIGDIR=/tmp/epistemia-mpl-cache XDG_CACHE_HOME=/tmp/epistemia-cache`.
