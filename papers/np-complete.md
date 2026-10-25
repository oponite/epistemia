---
title: "Finding Minimum-Cardinality Subsets: From Pair Search to Bidirectional Layers"
author: "Vijay Neelakantan"
date: "2026-10-21"
description: "An investigation of minimum-cardinality subset sum through pair-first solving, reusable partial-sum layers, and bidirectional search."
---

Given a sorted set of distinct, strictly positive integers

$$
X=\{x_1,x_2,\ldots,x_n\}
$$

and an integer target $T$, determine whether a subset $S\subseteq X$ sums to $T$. If one exists, determine its minimum cardinality:

$$
k^*=\min\left\{|S|:S\subseteq X,\ \sum_{x\in S}x=T\right\}.
$$

The general formulation permits every subset size, including the empty set and the full input. For $T=0$, the empty subset is optimal. Negative targets have no solution because every input value is positive.

The central question of this investigation is how to establish the smallest feasible cardinality while avoiding repeated computation.

I developed and evaluated a bidirectional prototype for exact minimum-cardinality subset sum. It combines cardinality-indexed earliest-ending states, forward search for retained elements, backward search for omitted elements, and explicit stopping conditions that certify optimality. The contribution examined here is this particular combination, its correctness analysis, and its measured behavior.

## Origin of the investigation

This investigation began with a day spent reading Wikipedia’s article on the P versus NP problem. My aim was to explore whether I could develop an approach toward proving P=NP. Codex suggested subset sum as an example of an NP-complete problem. I chose to pursue it because I find sets of integers intuitive to manipulate mentally: I could construct examples, reason about combinations, and examine how changes to the constraints affected possible solutions.

I remained focused on subset sum as the investigation developed. I also read Wikipedia’s treatment of the subset sum problem, extending my own background research beyond the original article on P versus NP. The initial note examined minimum-cardinality subset sum under a bounded-target restriction.

I designed and directed this investigation using Codex as a tool throughout its development and writing. I proposed successive changes, challenged repeated computation, selected comparisons, and requested implementations and experiments. I read and verified every line produced during that process. Tool-assisted development forms part of my research method.

## Starting with a bounded target

The original formulation imposed two additional restrictions:

1. The solution must contain between $2$ and $n-1$ elements.
2. The target must satisfy $T<n$.

A minimum-count dynamic program solves this restricted problem. For positive $T$, discard values greater than or equal to $T$, initialize $\operatorname{dp}[0]=0$, and set all other entries to infinity. For each remaining value $x$, update sums in descending order:

$$
\operatorname{dp}[s]
=
\min\left(\operatorname{dp}[s],\ 1+\operatorname{dp}[s-x]\right).
$$

Descending updates prevent using an element more than once. After processing every element, a finite $\operatorname{dp}[T]$ gives the minimum count.

Discarding values equal to $T$ excludes singleton answers. Positivity and $T<n$ ensure that any remaining solution contains fewer than $n$ elements.

The count-only algorithm uses $O(nT)$ time and $O(T)$ space under unit-cost arithmetic. Consequently, $T<n$ gives an $O(n^2)$ operation bound. For unrestricted targets, dependence on the numeric value of $T$ is pseudo-polynomial: writing $T$ in binary requires only $O(\log T)$ bits. This distinction is part of the standard analysis of subset sum. [Cornell lecture notes](https://courses.cs.cornell.edu/cs4820/2018fa/lectures/subset_sum.pdf)

This established a baseline. I then focused on whether the minimum-cardinality requirement itself could justify an earlier answer.

## Using a pair to establish optimality

Under the original size restriction, every permitted solution contains at least two elements. A valid pair therefore establishes both feasibility and optimality:

$$
x_i+x_j=T
\quad\Longrightarrow\quad
k^*=2,
$$

provided the pair is an eligible proper subset.

I chose to exploit this lower bound before invoking the general dynamic program.

On sorted input, two pointers find a pair in $O(n)$ operations:

1. Place one pointer at the smallest element and the other at the largest.
2. If their sum equals $T$, return the pair.
3. If the sum is too small, advance the left pointer.
4. If the sum is too large, retreat the right pointer.
5. Stop when the pointers meet.

Each move eliminates an endpoint that cannot participate in a pair within the remaining interval. At most $n-1$ moves are needed.

The resulting hybrid first searches for a pair and falls back to DP when no pair exists. Pair failure means only that no eligible two-element answer exists; a larger solution may remain.

Experiment C replayed 30 inputs at six sizes from $100$ to $4{,}000$, with $T=n-1$. Every input had an eligible pair. At $n=4{,}000$, median times were:

| Method | Milliseconds per call |
|---|---:|
| DP with reconstruction | 4.356016 |
| Pair search | 0.706228 |
| Hybrid with reconstruction | 0.706996 |
| Certificate verification | 0.589715 |

The hybrid was **6.161× faster than DP** on this cohort. Pair and hybrid timing fits both had exponent $p=1.001$. The linear operation bound follows from the pointer argument independently of the timing fit.

I next removed the subset-size restriction and requested a separate experiment. This changed the optimality argument: a pair is minimum only after excluding a singleton, while target zero has an empty optimum.

The revised hybrid therefore checks:

$$
\text{empty solution}
\rightarrow
\text{singleton}
\rightarrow
\text{pair}
\rightarrow
\text{DP fallback}.
$$

Replaying the original 30 inputs produced **eight singleton optima and 22 pair optima**. The broader experiment also included controlled three-element and impossible cases. It retained $T=n-1$, isolating the change in permitted subset sizes.

## Extending the search across cardinalities

I then proposed extending pair search to larger answers.

For a fixed cardinality $k$, one complete method is:

1. Choose $k-2$ fixed elements.
2. Subtract their sum from $T$.
3. Search for the remaining pair among elements after the fixed indices.
4. Repeat for every eligible fixed combination.

Searching only later indices prevents element reuse. Completeness follows because every sorted $k$-element solution has a prefix of $k-2$ elements followed by a final pair.

For fixed $k$, this gives an $O(n^{k-1})$ operation bound. Searching cardinalities in ascending order returns a minimum solution, but the work grows combinatorially when the required cardinality grows.

I proposed Fibonacci limits to organize the search. An endpoint-first order such as

$$
2,3,5,4,8,6,7,\ldots
$$

can inspect a larger cardinality before a smaller one. A successful endpoint is therefore only a candidate until the skipped smaller sizes have been excluded. Failure at one exact cardinality does not exclude another.

The measurements exposed the cost of this ordering. On four-element-optimum inputs, an endpoint-first variant could spend substantial time unsuccessfully searching size five before reaching size four.

I questioned that work and revised the rule: arrive at the Fibonacci endpoint, but hold it until the intervening smaller sizes have been checked.

```text
Arrive at 2:  check 2
Arrive at 3:  check 3
Arrive at 5:  check 4, then 5 if needed
Arrive at 8:  check 6, then 7, then 8 if needed
```

The resulting search order is ascending, grouped into Fibonacci phases. A size-four success stops before size five is searched.

At $n=20$, the revised phase method took **0.013417 ms** on the four-element group, compared with **0.013173 ms** for ordinary ascending search. The earlier large gap disappeared. Both methods now perform the same exact-cardinality searches; the Fibonacci boundaries supply organization rather than additional pruning.

## Reusing partial results across cardinalities

My next question concerned the repeated work inside those searches. If smaller subsets had already been considered, why should each new cardinality begin again?

This motivated the transition to incremental partial-sum layers.

After excluding values greater than $T$, let the retained sorted input be

$$
Y=\{y_0,y_1,\ldots,y_{m-1}\}.
$$

A layer for cardinality $k$ stores:

$$
L_k[s]
=
\text{the smallest ending index of a }k\text{-element subset summing to }s.
$$

The implementation represents this as:

```python
layer[partial_sum] = earliest_ending_index
```

To construct the next layer:

1. Take each stored sum $s$ and ending index $j$.
2. Add each element $y_i$ with $i>j$.
3. Discard sums exceeding $T$.
4. For equal new sums, retain the smallest ending index.
5. Return the new cardinality if the layer contains $T$.

A separate next-layer dictionary prevents adding multiple elements during one transition.

### Why the compression is safe

Suppose two $k$-element subsets have the same sum, but end at indices $a<b$. Every element available after $b$ is also available after $a$. The state ending at $a$ therefore permits every continuation available from the state ending at $b$.

Keeping the earlier endpoint preserves future possibilities.

For example, with $Y=[1,2,3,4]$, the pairs $\{1,4\}$ and $\{2,3\}$ both sum to five. Retaining the latter leaves four available, allowing the next layer to reach nine.

Completeness follows inductively. Take any feasible subset and remove its last element. Its prefix sum is represented in the preceding layer by an endpoint no later than that prefix’s actual endpoint. The last element remains available for extension.

Because cardinalities are processed ascending, the first layer containing $T$ gives the minimum count. If a layer is empty, no larger feasible subset can exist: every larger subset would have a smaller prefix with sum at most $T$.

The public layered solver is count-only. For example:

```python
solve_fibonacci_layers([1, 6, 11, 16, 21, 26], 34)
# (None, 4)
```

This already establishes YES and an optimum of four. The search does not require a subsequent two-pointer stage to decide existence.

Under unit-cost arithmetic and expected constant-time hashing, the implementation has an $O(n^2T)$ time bound and $O(n+T)$ extra-space bound. Each layer has at most $T$ positive sums, each state can attempt up to $n$ extensions, and there are at most $n$ layers.

A more informative time bound counts the states actually expanded. Let $\mathcal K$ contain the cardinalities whose layers are used to construct a successor layer. Under the same arithmetic and hashing assumptions, the expected running time is

$$
O\!\left(n+n\sum_{k\in\mathcal K}|L_k|\right).
$$

The initial $n$ accounts for validation and initialization. Each stored state attempts at most $n$ extensions. Equal-sum compression reduces the number of states in a layer, while early termination reduces the number of layers expanded. A final layer that supplies the answer is constructed but is not itself expanded. Bounding the sum by $nT$ recovers the coarser $O(n^2T)$ bound.

The substantive change is reuse of compressed partial results. Fibonacci boundaries remain part of the scheduling, but do not supply that compression.

## Searching from both ends

I subsequently proposed running the layer method from both ends of the possible cardinalities.

After handling trivial targets and filtering values above $T$, define

$$
A=\sum_{y\in Y}y,
\qquad
U=A-T.
$$

For every retained subset $S$,

$$
\sum_{y\in S}y=T
\quad\Longleftrightarrow\quad
\sum_{y\in Y\setminus S}y=U.
$$

Consequently,

$$
\min_{\sum S=T}|S|
=
m-\max_{\sum R=U}|R|.
$$

Forward search builds retained subsets of increasing cardinality. Backward search builds omitted subsets of increasing cardinality, corresponding to progressively smaller retained answers.

The backward objective is to maximize omissions. Its first success gives a candidate, not necessarily the optimum.

The prototype alternates individual layers, forward first, and retains the best backward candidate. If forward has completely checked retained sizes through $f$, and backward has completely checked omission sizes through $r$, then

$$
f+r\ge m-1
$$

leaves no unchecked cardinality. The best candidate can then be returned, or NO if neither direction found one.

Positivity supplies additional bounds. Let $L$ be the smallest count whose largest elements can sum to at least $T$. Any answer contains at least $L$ elements, so backward search need not exceed $m-L$ omissions. An empty omission layer also excludes every larger omission count.

For the bidirectional prototype, let $F_k$ and $B_r$ be the forward and backward state dictionaries, and let $\mathcal K_F$ and $\mathcal K_B$ index the layers actually expanded in each direction. The corresponding expected time bound is

$$
O\!\left(n+n\sum_{k\in\mathcal K_F}|F_k|
          +n\sum_{r\in\mathcal K_B}|B_r|\right).
$$

Searching from both ends can avoid expanding large forward layers when the omission search supplies an earlier stopping certificate. It also incurs backward work. The extension counts below measure that tradeoff directly; the later worst-case construction shows how large the stored layers can still become.

For the input

```text
X = [2,3,6,7,10,14,29,30,31,34,
     36,41,42,43,45,46,50,52,58,59]
T = 621
```

the total is $638$, making $U=17$. Either $\{3,14\}$ or $\{7,10\}$ can be omitted. No triple sums to 17, and the four smallest elements already sum to 18. Thus the maximum omission count is two, and the minimum retained count is **18**.

The alternating prototype used **2,091 counted extensions**, compared with **17,539** for the forward-only prototype: **8.39× fewer extensions**. These are operation counts, not elapsed-time measurements.

## Experiments and validation

I requested comparative benchmarks after implementation, then specifically asked for inputs where DP performed better. This made the choice of comparator consequential.

The count-only layer study measured 120 seeded inputs across six groups at $n=8,12,16,20$. At $n=20$:

| Group | Ascending combinations | Incremental layers | DP |
|---|---:|---:|---:|
| Full-set optimum | 87.558041 ms | 0.733132 ms | 0.023699 ms |
| No solution | 0.072415 ms | 0.009797 ms | 0.011590 ms |
| Four-element optimum | 0.012972 ms | 0.018237 ms | 0.019330 ms |

Layers were **119.43× faster than ascending combination search** on the full-set group, while remaining **30.93× slower than DP**. On the impossible group, layers were **7.39× faster than ascending**. Ascending remained faster on the four-element group.

The all-sizes hybrid also showed the cost of unsuccessful early paths. At $n=4{,}000$, it was **5.27× faster than DP** on pair-optimum inputs, but **36.53% slower** on the controlled three-element group.

The timed studies used seeded inputs and preserved previous results. C and subsequent studies used warm-up, doubling calibration toward 20 ms batches with a 65,536-call cap, and five measured batches. Timings include public validation and result construction. Generation, calibration, external correctness checks, and file writing are excluded. Reported size times are medians of per-input medians.

These families have controlled answers. Full-set targets equal the input total, and impossible cases use even inputs against odd targets. Direct checks can recognize those conditions. The measurements compare the stated implementations rather than establish intrinsic difficulty.

The bidirectional comparison gave both temporary variants the same shortcuts and bounds. Across the existing 120 inputs, alternating directions used fewer extensions on **zero**, the same on **67**, and more on **53**. Its advantage in the near-full example therefore depends on the input.

The latest verification passed **3,289 repository tests**. Both temporary prototypes also matched exhaustive enumeration on **5,376 inputs each** and returned the expected answer on all 120 seeded cases.

## A worst-case limitation

The subsequent analysis with Codex identified a limitation that measurements on small targets did not reveal: a layer can contain exponentially many distinct sums.

For even $n=2q\ge6$, consider

$$
X=\{1,2,4,\ldots,2^{n-1}\},
\qquad
T=2^{n-1}+2^{q-1}-1.
$$

The unique solution contains the largest element and the smallest $q-1$ elements. Its optimum cardinality is $q$.

The first $n-1$ elements together sum to

$$
2^{n-1}-1<T.
$$

Therefore every $(q-1)$-element subset of those elements survives the target cutoff. Powers of two give every distinct subset a distinct sum, so equal-sum compression merges none of these states.

Before reaching the optimum, the forward layer must contain at least

$$
\binom{n-1}{q-1}
=
\Theta\!\left(\frac{2^n}{\sqrt n}\right)
$$

entries.

The alternating prototype encounters the same obstruction. The unique omitted complement also contains $q$ elements. Neither direction finds an earlier solution, and the implemented stopping rules do not terminate before this large forward layer is constructed.

Traces of both implementations confirmed:

| $n$ | Target | Optimum | Entries in the preceding forward layer |
|---:|---:|---:|---:|
| 8 | 135 | 4 | 38 |
| 12 | 2,079 | 6 | 467 |
| 16 | 32,895 | 8 | 6,442 |
| 20 | 524,799 | 10 | 92,387 |

With ordinary explicit binary encoding, these inputs require $B=\Theta(n^2)$ bits. The forced state count is consequently

$$
2^{\Omega(\sqrt B)},
$$

which exceeds every fixed polynomial in $B$.

This establishes a superpolynomial worst case for the current explicit-layer implementations. The obstruction occurs before the successful layer, so returning earlier during construction of that final layer would not remove it.

Powers-of-two inputs themselves admit efficient specialized solutions. The result identifies a limitation of these implementations, not a lower bound for every subset-sum algorithm.

## Relation to earlier methods

The closest state-representation antecedent located in the review is Bob Weems's [2016 notes, §7.F](https://ranger.uta.edu/~weems/NOTES5311/NEWNOTES/notes00.pdf), which represent a reachable sum by its smallest ending index and extend it using later input elements. His [Fall 2020 assignment](https://ranger.uta.edu/~weems/NOTES3318/LAB/LAB3FALL20/lab3fall20.pdf) explicitly asks for cardinality to be added as another parameter, although it does not supply a complete two-dimensional implementation. The present solver evaluates cardinality layers using sparse dictionaries, retains only consecutive layers, and stops at the first successful cardinality.

Complementary targets also have direct precedents. [O'Neil's 2013 empirical study, §2](https://micsymposium.org/mics_2013_Proceedings/submissions/mics20130_submission_13.pdf) replaces a target with the input total minus that target when this reduces the search range. The prototype here uses the complementary target to maximize omitted cardinality, alternating that search with minimum retained-cardinality search and applying explicit coverage and optimality stopping conditions. More broadly, sparse reachable-sum computation and its dependence on the number of represented sums are discussed by [Bringmann, Fischer, and Nakos](https://arxiv.org/html/2410.21942v1).

A targeted literature review through 25 October 2026 identified antecedents for individual components but did not locate an earlier description of the complete alternating retained/omitted-cardinality design with the same state representation and termination policy. This finding identifies the scope of the combination examined here; it does not establish historical priority.

## What this investigation establishes

The investigation connects several distinct mechanisms: using a cardinality lower bound to certify an early optimum, ordering exact-cardinality searches, reusing partial sums, and searching omitted complements.

My contribution includes the algorithm-design decisions throughout this progression: choosing subset sum as the working problem, removing restrictions, revising the search order, challenging repeated computation, proposing bidirectional layers, and selecting comparisons that included cases where DP won. I used Codex in developing and writing the representations, implementations, tests, and proofs, and read and verified the resulting work.

A polynomial-time algorithm for general subset sum would establish P=NP. A minimum-cardinality algorithm would suffice because its count immediately decides existence. The relevant requirement is a polynomial worst-case bound in encoded input length. [Stephen Cook’s problem statement](https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf)

The current methods establish correctness and specified improvements in computational work, while the explicit input family above rules out that polynomial guarantee for these implementations. The remaining algorithmic question is whether many different reachable sums can be handled without storing and extending each one individually, while preserving exact feasibility and minimum cardinality.
