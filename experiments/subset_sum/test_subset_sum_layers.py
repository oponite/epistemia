"""Independent checks for reusable exact-cardinality partial-sum layers."""

from itertools import combinations
import random

import numpy as np
import pytest

from subset_sum_all_sizes import brute_force
from subset_sum_cardinality import _extend_layer, solve_fibonacci_layers


@pytest.mark.parametrize('case', range(500))
def test_layers_against_seeded_enumeration(case):
    rng = random.Random(20261033 + case)
    values = sorted(rng.sample(range(1, 41), rng.randrange(13)))
    target = rng.randint(-3, sum(values) + 3)
    original = values.copy()
    assert solve_fibonacci_layers(values, target) == (None, brute_force(values, target)[1])
    assert values == original


@pytest.mark.parametrize('values,target,count', [
    ([], 0, 0), ([], 1, None), ([], -1, None), ([1, 2], -1, None),
    ([1, 2], 0, 0), ([5], 5, 1), ([5], 4, None), ([5], 6, None),
    ([2, 3, 5], 5, 1), ([2, 3], 5, 2), ([1, 2, 3, 4], 9, 3),
    ([1, 6, 11, 16, 21, 26], 34, 4), ([1, 2, 4, 8], 15, 4),
    ([1, 4, 10], 8, None), ([1, 2, 4, 10], 9, None),
    ([2, 4, 6, 8], 9, None), ([1, 2, 10**100], 3, 2),
    ([10**100], 10**100, 1), ([10**100, 10**100 + 1], 2 * 10**100 + 1, 2),
])
def test_layers_boundaries(values, target, count):
    original = values.copy()
    assert solve_fibonacci_layers(values, target) == (None, count)
    assert values == original


@pytest.mark.parametrize('values', [[2, 1], [1, 1], [0, 1], [-1, 1], [True, 2], [1, 2.0], None])
def test_layers_invalid_inputs(values):
    with pytest.raises(ValueError):
        solve_fibonacci_layers(values, 0)


@pytest.mark.parametrize('target', [True, 1.0, '3', None])
def test_layers_invalid_targets(target):
    with pytest.raises(ValueError):
        solve_fibonacci_layers([1, 2, 3], target)


def test_layers_numpy_integers_and_immutability():
    values = np.array([1, 2**63, 2**63 + 2], dtype=np.uint64)
    original = values.copy()
    assert solve_fibonacci_layers(values, 2**63 + 1) == (None, 2)
    np.testing.assert_array_equal(values, original)
    values = np.array([1, 2, 4, 8])
    original = values.copy()
    assert solve_fibonacci_layers(values, np.int64(15)) == (None, 4)
    np.testing.assert_array_equal(values, original)


def test_layers_exhaustive_small_universe():
    checks = 0
    for mask in range(256):
        values = [i + 1 for i in range(8) if mask >> i & 1]
        expected = {}
        for k in range(len(values) + 1):
            for subset in combinations(values, k):
                expected.setdefault(sum(subset), k)
        for target in range(-1, sum(values) + 2):
            assert solve_fibonacci_layers(values, target) == (None, expected.get(target))
            checks += 1
    assert checks == 5376


@pytest.mark.parametrize('values,target', [
    ([1, 2, 3, 4], 9), ([1, 2, 3, 4, 5, 9], 14),
    (list(range(1, 9)), 36), ([2, 4, 6, 8], 9),
])
def test_each_compressed_layer_matches_independent_subsets(values, target):
    layer = {value: i for i, value in enumerate(values)}
    original_values = values.copy()
    for k in range(2, len(values) + 1):
        previous = layer.copy()
        next_layer = _extend_layer(values, layer, target)
        expected = {}
        for indices in combinations(range(len(values)), k):
            total = sum(values[i] for i in indices)
            if total <= target:
                expected[total] = min(indices[-1], expected.get(total, len(values)))
        assert next_layer == expected
        assert layer == previous and values == original_values
        layer = next_layer


def test_earliest_endpoint_preserves_later_extension():
    values = [1, 2, 3, 4]
    pairs = _extend_layer(values, {value: i for i, value in enumerate(values)}, 9)
    # Sum five can end at index three via 1+4, but 2+3 leaves four available.
    assert pairs[5] == 2
    assert _extend_layer(values, pairs, 9)[9] == 3
    assert _extend_layer([2], {2: 0}, 4) == {}


@pytest.mark.parametrize('values,target,count,extensions', [
    ([1, 6, 11, 16, 21, 26], 34, 4, 3),
    ([1, 2, 4, 8, 16, 32, 64], 127, 7, 6),
    ([2, 4, 6, 8], 9, None, 2),
    ([], 0, 0, 0), ([5], 5, 1, 0), ([5], -1, None, 0),
])
def test_layers_reuse_previous_output_and_stop(monkeypatch, values, target, count, extensions):
    import subset_sum_cardinality as search
    extend = search._extend_layer
    inputs, outputs = [], []

    def traced(values, layer, target):
        inputs.append(layer)
        result = extend(values, layer, target)
        outputs.append(result)
        return result

    def forbidden(*args, **kwargs):
        pytest.fail('Layer search must not restart the exact-k combination search')

    monkeypatch.setattr(search, '_extend_layer', traced)
    monkeypatch.setattr(search, '_search_exact', forbidden)
    assert search.solve_fibonacci_layers(values, target) == (None, count)
    assert len(outputs) == extensions
    assert all(inputs[i] is outputs[i - 1] for i in range(1, len(inputs)))
    if count == 4:
        assert outputs[-2][18] == 2 and target in outputs[-1]
    if count is None and extensions:
        assert outputs[-1] == {}
