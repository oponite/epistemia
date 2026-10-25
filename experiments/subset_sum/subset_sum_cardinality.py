"""Exact cardinality search using combinations or reusable partial-sum layers."""

from itertools import combinations

if __package__:
    from .subset_sum import _validate
else:
    from subset_sum import _validate


def _search_exact(values, T, k, reconstruct):
    m = len(values)
    for fixed in combinations(range(m - 2), k - 2):
        remaining = T - sum(values[i] for i in fixed)
        left, right = (fixed[-1] + 1 if fixed else 0), m - 1
        while left < right:
            total = values[left] + values[right]
            if total == remaining:
                subset = [values[i] for i in fixed] + [values[left], values[right]] if reconstruct else None
                return subset, k
            if total < remaining:
                left += 1
            else:
                right -= 1
    return None, None


def solve_cardinality(X, T, reconstruct=True):
    """Return the smallest subset and count, or (None, None) after exhaustion.

    All subset sizes are allowed. Fixed-k search takes O(n**(k-1)) work;
    searching all sizes has combinatorial worst-case cost. No DP fallback.
    Extra space is O(n), including filtered values and combination state.
    """
    _validate(X, T)
    T = int(T)
    if T < 0:
        return None, None
    if T == 0:
        return ([] if reconstruct else None), 0
    values = [int(x) for x in X if int(x) <= T]
    if T in values:
        return ([T] if reconstruct else None), 1
    m = len(values)
    for k in range(2, m + 1):
        result = _search_exact(values, T, k, reconstruct)
        if result[1] is not None:
            return result
    return None, None


def solve_fibonacci(X, T, reconstruct=True):
    """Try Fibonacci sizes, then exhaust skipped smaller sizes in ascending order.

    An exact-size failure cannot rule out smaller sizes. The first Fibonacci
    success is only a candidate until all smaller sizes have been checked.
    Worst-case cost remains combinatorial; extra space is O(n).
    """
    _validate(X, T)
    T = int(T)
    if T < 0:
        return None, None
    if T == 0:
        return ([] if reconstruct else None), 0
    values = [int(x) for x in X if int(x) <= T]
    if T in values:
        return ([T] if reconstruct else None), 1
    m = len(values)
    checked = set()
    candidate = (None, None)
    k, following = 2, 3
    while k <= m:
        candidate = _search_exact(values, T, k, reconstruct)
        checked.add(k)
        if candidate[1] is not None:
            break
        k, following = following, k + following
    stop = candidate[1] if candidate[1] is not None else m + 1
    for k in range(2, stop):
        if k not in checked:
            result = _search_exact(values, T, k, reconstruct)
            if result[1] is not None:
                return result
    return candidate


def solve_fibonacci_gaps(X, T, reconstruct=True):
    """Search each Fibonacci phase ascending, holding its endpoint until last.

    The first success is optimal because all smaller sizes have failed. This
    performs the same exact-k searches as ordinary ascending order, grouped
    into phases. Worst-case cost is combinatorial and extra space is O(n).
    """
    _validate(X, T)
    T = int(T)
    if T < 0:
        return None, None
    if T == 0:
        return ([] if reconstruct else None), 0
    values = [int(x) for x in X if int(x) <= T]
    if T in values:
        return ([T] if reconstruct else None), 1
    m = len(values)
    previous, endpoint, following = 1, 2, 3
    while endpoint <= m:
        for k in range(previous + 1, endpoint + 1):
            result = _search_exact(values, T, k, reconstruct)
            if result[1] is not None:
                return result
        previous, endpoint, following = endpoint, following, endpoint + following
    for k in range(previous + 1, m + 1):
        result = _search_exact(values, T, k, reconstruct)
        if result[1] is not None:
            return result
    return None, None


def _extend_layer(values, layer, T):
    """Add one later element; equal sums retain the earliest ending index."""
    next_layer = {}
    m = len(values)
    for subtotal, last_index in layer.items():
        for i in range(last_index + 1, m):
            total = subtotal + values[i]
            if total > T:
                break
            # An earlier endpoint leaves every extension of a later endpoint available.
            if i < next_layer.get(total, m):
                next_layer[total] = i
    return next_layer


def solve_fibonacci_layers(X, T):
    """Return (None, minimum_count), or (None, None) if no subset sums to T.

    Each cardinality extends the preceding partial-sum layer by one element.
    A state keeps the earliest ending index for its sum and cardinality;
    only later indices can extend it. Fibonacci limits group ascending sizes.
    All subset sizes are allowed. This API is count-only and never calls the
    two-pointer search or DP comparator. For positive T, expected time is
    O(n**2 * T), space O(n + T), under unit-cost arithmetic and hashing.
    These bounds depend on numeric T and are pseudo-polynomial.
    """
    _validate(X, T)
    T = int(T)
    if T < 0:
        return None, None
    if T == 0:
        return None, 0
    values = [int(x) for x in X if int(x) <= T]
    if T in values:
        return None, 1
    m = len(values)
    layer = {value: i for i, value in enumerate(values)}
    previous, endpoint, following = 1, 2, 3
    while previous < m:
        for k in range(previous + 1, min(endpoint, m) + 1):
            layer = _extend_layer(values, layer, T)
            if T in layer:
                return None, k
            if not layer:
                return None, None
        previous, endpoint, following = endpoint, following, endpoint + following
    return None, None
