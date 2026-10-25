"""Minimum-cardinality 0/1 Subset Sum for distinct positive integers."""

from itertools import combinations
from numbers import Integral

import numpy as np


def _validate(X, T):
    if isinstance(T, bool) or not isinstance(T, Integral):
        raise ValueError("T must be an integer")
    try:
        len(X)
        previous = 0
        for value in X:
            if (
                isinstance(value, bool)
                or not isinstance(value, Integral)
                or value <= previous
            ):
                raise ValueError("X must contain sorted, distinct, positive integers")
            previous = value
    except TypeError as error:
        raise ValueError("X must be a finite integer sequence") from error


def solve(X, T, reconstruct=True):
    """Return (minimum subset, count), (None, count), or (None, None).

    With reconstruct=False, only the count is returned. Invalid inputs raise
    ValueError. X is never modified. Time is O(nT); rolling space is O(T).
    Recording reconstruction choices additionally costs O(mT) boolean space,
    where m is the number of input elements strictly below T.
    """
    _validate(X, T)
    T = int(T)
    if T <= 0:
        return None, None
    Y = [int(value) for value in X if value < T]
    dp = np.full(T + 1, np.inf)
    dp[0] = 0
    improved = np.zeros((len(Y), T + 1), dtype=bool) if reconstruct else None
    for index, value in enumerate(Y):
        if reconstruct:
            improved[index, value:] = dp[:-value] + 1 < dp[value:]
        # The entire RHS uses old dp before assignment, so each item is used at most once.
        dp[value:] = np.minimum(dp[value:], dp[:-value] + 1)
    if not 2 <= dp[T] <= len(X) - 1:
        return None, None
    count = int(dp[T])
    if not reconstruct:
        return None, count
    subset = []
    remaining = T
    for index in range(len(Y) - 1, -1, -1):
        if improved[index, remaining]:
            subset.append(Y[index])
            remaining -= Y[index]
    assert remaining == 0 and len(subset) == count
    subset.reverse()
    return subset, count


def solve_pair(X, T):
    """Return (sorted_pair, 2), or (None, None) when no eligible pair exists.

    A valid pair is optimal because eligible subsets have at least two items.
    On sorted input, time is O(n) and extra space O(1) under unit-cost arithmetic.
    Failure does not rule out a larger solution. X is neither copied nor sorted.
    """
    _validate(X, T)
    T = int(T)
    if T <= 0 or len(X) < 3:
        return None, None
    left, right = 0, len(X) - 1
    while left < right:
        low, high = int(X[left]), int(X[right])
        total = low + high
        if total == T:
            return [low, high], 2
        if total < T:
            left += 1
        else:
            right -= 1
    return None, None


def solve_hybrid(X, T, reconstruct=True):
    """Try an optimal pair in O(n), then use DP if no eligible pair exists.

    Return format matches solve, including count-only mode. Positive-target
    worst-case time remains O(nT); fallback deliberately reuses DP validation.
    """
    subset, count = solve_pair(X, T)
    if count is not None:
        return (subset if reconstruct else None), count
    return solve(X, T, reconstruct)


def verify(X, T, S):
    """Check a feasible certificate, including an arbitrary ordering of S.

    Expected O(n) time and O(n) space under unit-cost integer hashing, with
    no cached membership set. This does not certify minimum cardinality.
    Malformed instances and certificates return False.
    """
    try:
        _validate(X, T)
        if S is None or not 2 <= len(S) <= len(X) - 1:
            return False
        if any(isinstance(value, bool) or not isinstance(value, Integral) for value in S):
            return False
        members = set(S)
        return (
            len(members) == len(S)
            and members.issubset(set(X))
            and sum(int(value) for value in S) == T
        )
    except (TypeError, ValueError):
        return False


def brute_force(X, T):
    """Independent exhaustive oracle for small tests; same return format as solve."""
    _validate(X, T)
    if T <= 0:
        return None, None
    values = [int(value) for value in X]
    for count in range(2, len(values)):
        for subset in combinations(values, count):
            if sum(subset) == T:
                return list(subset), count
    return None, None
