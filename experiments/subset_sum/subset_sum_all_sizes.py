"""Separate minimum-cardinality experiment allowing empty and full subsets."""

from itertools import combinations
from numbers import Integral

import numpy as np

if __package__:
    from .subset_sum import _validate
else:
    from subset_sum import _validate


def solve(X, T, reconstruct=True):
    """Return (minimum subset, count), or (None, None) if no solution exists.

    Count-only success returns (None, count). Empty and full subsets are valid.
    Positive-target DP uses O(nT) time and O(T) rolling space; reconstruction
    adds O(mT) choice storage, where m counts values at most T.
    """
    _validate(X, T)
    T = int(T)
    if T < 0:
        return None, None
    if T == 0:
        return ([] if reconstruct else None), 0
    values = [int(value) for value in X if value <= T]
    dp = np.full(T + 1, np.inf)
    dp[0] = 0
    improved = np.zeros((len(values), T + 1), dtype=bool) if reconstruct else None
    for index, value in enumerate(values):
        if reconstruct:
            improved[index, value:] = dp[:-value] + 1 < dp[value:]
        # The complete RHS uses the previous table, preventing repeated item use.
        dp[value:] = np.minimum(dp[value:], dp[:-value] + 1)
    if not np.isfinite(dp[T]):
        return None, None
    count = int(dp[T])
    if not reconstruct:
        return None, count
    subset, remaining = [], T
    for index in range(len(values) - 1, -1, -1):
        if improved[index, remaining]:
            subset.append(values[index])
            remaining -= values[index]
    assert remaining == 0 and len(subset) == count
    subset.reverse()
    return subset, count


def solve_hybrid(X, T, reconstruct=True):
    """Check zero, singleton, and pair solutions before falling back to DP.

    Early paths validate once and use O(n) time and O(1) extra space under
    unit-cost arithmetic. DP fallback validates again and retains O(nT) time.
    """
    _validate(X, T)
    T = int(T)
    if T < 0:
        return None, None
    if T == 0:
        return ([] if reconstruct else None), 0
    if any(int(value) == T for value in X):
        return ([T] if reconstruct else None), 1
    left, right = 0, len(X) - 1
    while left < right:
        low, high = int(X[left]), int(X[right])
        total = low + high
        if total == T:
            return ([low, high] if reconstruct else None), 2
        if total < T:
            left += 1
        else:
            right -= 1
    return solve(X, T, reconstruct)


def verify(X, T, S):
    """Check feasibility, including empty and full subsets; not optimality.

    Expected O(n) time/space under unit-cost hashing. Malformed inputs return
    False; all additions use Python integers to avoid NumPy integer overflow.
    """
    try:
        _validate(X, T)
        if S is None or not 0 <= len(S) <= len(X):
            return False
        if any(isinstance(value, bool) or not isinstance(value, Integral) for value in S):
            return False
        members = set(S)
        return (
            len(members) == len(S)
            and members.issubset(set(X))
            and sum(int(value) for value in S) == int(T)
        )
    except (TypeError, ValueError):
        return False


def brute_force(X, T):
    """Independent exhaustive reference, considering subset sizes 0 through n."""
    _validate(X, T)
    T = int(T)
    values = [int(value) for value in X]
    for count in range(len(values) + 1):
        for subset in combinations(values, count):
            if sum(subset) == T:
                return list(subset), count
    return None, None
