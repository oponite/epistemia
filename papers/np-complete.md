---
title: "Solving a Polynomial-Time Case of an NP-complete Problem: Minimum-Cardinality Subset Sum with a Bounded Target"
author: "Vijay Neelakantan"
date: "2026-10-21"
description: "An exact dynamic program for minimum-cardinality subset sum with a target smaller than the input set size."
---
Given a sorted set of integers $X = \{x_1, x_2, \dots, x_n\}$, where every single $x_i$ is strictly positive ($x_i > 0$) and a target integer $T$, determine whether there exists a subset $S \subset X$ such that:

1. The sum of all elements in $S$ equals $T$.
2. The subset contains any number of elements from $2$ to $n-1$.
3. The subset exhibits minimum cardinality.
4. $T$ < $n$

Formally:

**Input:** A sorted set $X$ of $n$ strictly positive integers and a target integer $T<n$.

**Output:** YES if there exists a subset $S$ satisfying both:

- $\sum_{x \in S} x = T$
- $2 \le |S| \le n - 1$

Otherwise, output NO.

## Potential Solution

1. If $T\leq 0$, return **NO**: strictly positive integers cannot sum to a nonpositive target.
2. Create $Y = \{y_1, y_2, \dots, y_m\}$ by removing all elements greater than or equal to $T$ from $X$. Here, $m=|Y|$; $n$ remains the size of $X$.
3. Initialize a table $\operatorname{dp}[0\dots T]$ with $\operatorname{dp}[0]=0$ and all other entries set to $\infty$. Each entry stores the fewest elements needed to reach that sum using the numbers processed so far. The value $\infty$ means the sum is unreachable.
4. Process each $y_i$ once. For sums $s$ from $T$ down to $y_i$, update:

   $$
   \operatorname{dp}[s] = \min\bigl(\operatorname{dp}[s],\;1+\operatorname{dp}[s-y_i]\bigr).
   $$

   The first option excludes $y_i$; the second includes it. Updating sums downward prevents using the same element more than once.
5. If $\operatorname{dp}[T]=\infty$, return **NO**. Otherwise, return **YES**; $\operatorname{dp}[T]$ is the minimum cardinality.

Removing elements greater than or equal to $T$ preserves every eligible solution. Every remaining element is smaller than $T$, so a subset reaching $T$ must contain at least two elements. Since each element is at least $1$, the subset contains at most $T<n$ elements. Thus, a successful result satisfies $2\leq |S|\leq n-1$.

To recover a subset, also record whether each item strictly improves each table entry. Start at sum $T$ and trace the items backward. Whenever the recorded choice includes an item, select it and subtract its value from the current sum.

## What this solution establishes

The dynamic program uses $O(nT)$ time and $O(T)$ space for the minimum cardinality. Storing the choices needed to reconstruct a minimum-cardinality subset increases the space requirement to O(nT).

For unrestricted targets, this runtime is pseudo-polynomial: it depends on the value of $T$, not just its binary length.

**However, under the stated constraint $T<n$, the algorithm runs in $O(n²)$ time.** It requires $O(n)$ space to compute the minimum cardinality, or $O(n²)$ space when retaining reconstruction choices. This establishes an exact polynomial-time solution for the restricted problem; the polynomial guarantee depends on the bound on T.

Reference: [Cornell lecture notes on Subset Sum and pseudo-polynomial time](https://courses.cs.cornell.edu/cs4820/2018fa/lectures/subset_sum.pdf).
