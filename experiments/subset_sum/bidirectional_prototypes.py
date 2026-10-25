"""Forward-only and alternating prototypes used for the paper's operation counts.

Run this file without Python -O to reproduce the exhaustive and seeded checks.
The JSON report is written to stdout; no wall-clock measurements are made.
"""
from itertools import combinations
from collections import Counter, defaultdict
import json


def bounds_and_shortcuts(X, T):
    n = len(X)
    A = sum(X)
    if T < 0 or T > A:
        return True, None, None
    if T == 0:
        return True, 0, None
    if T in X:
        return True, 1, None
    if T == A:
        return True, n, None
    prefix = [0]
    for x in X:
        prefix.append(prefix[-1] + x)
    L = next(k for k in range(n + 1) if A-prefix[n-k] >= T)
    H = max(k for k in range(n + 1) if prefix[k] <= T)
    if L > H:
        return True, None, None
    return False, None, (A-T, L, H)


def extend(X, layer, cap, stats, direction):
    out = {}
    stats[direction+'_layers'] += 1
    for subtotal, last in layer.items():
        for i in range(last+1, len(X)):
            stats[direction+'_extensions'] += 1
            total = subtotal+X[i]
            if total > cap:
                break
            if i < out.get(total, len(X)):
                out[total] = i
    return out


def solve(X, T, bidirectional):
    """Return (minimum count, counters) for sorted distinct positive integers.

    These experimental variants assume validated inputs and return no witness.
    Both modes share filtering, shortcuts, bounds, and extension accounting.
    """
    X = tuple(x for x in X if x <= T)
    stats = dict(forward_layers=0, backward_layers=0,
                 forward_extensions=0, backward_extensions=0)
    shortcut, result, bounds = bounds_and_shortcuts(X,T)
    if shortcut:
        return result, stats
    U,L,H = bounds
    stats.update(L=L,H=H)
    F={x:i for i,x in enumerate(X)}
    B={0:-1}
    f,r=1,0
    stats.update(forward_layers=1, forward_extensions=len(X))
    best=None
    while f < H:
        f += 1
        F=extend(X,F,T,stats,'forward')
        if T in F:
            return f,stats
        if not F or f == H:
            return None,stats
        if not bidirectional:
            continue
        if f+r >= len(X)-1:
            return best,stats
        r += 1
        B=extend(X,B,U,stats,'backward')
        if U in B:
            best=len(X)-r
        if not B or r == len(X)-L or best == L or f+r >= len(X)-1:
            return best,stats
    return None,stats


def operations(stats):
    return stats['forward_extensions']+stats['backward_extensions']


def run_checks():
    from benchmark_cardinality import make_cases, make_input

    checks=0
    for n in range(9):
        for X in combinations(range(1,9),n):
            reference={}
            for k in range(n+1):
                for S in combinations(X,k):
                    reference.setdefault(sum(S),k)
            for T in range(-1,sum(X)+2):
                for bidirectional in (False,True):
                    count,stats=solve(X,T,bidirectional)
                    assert count == reference.get(T),(X,T,bidirectional,count,reference.get(T))
                checks+=1
    assert checks == 5376
    X=[2,3,6,7,10,14,29,30,31,34,36,41,42,43,45,46,50,52,58,59]
    T=621
    example={}
    for mode in (False,True):
        count,stats=solve(X,T,mode)
        assert count == 18
        example['bidirectional' if mode else 'forward']={**stats,'count':count,'total_extensions':operations(stats)}
    assert example['forward']['total_extensions'] == 17539
    assert example['bidirectional']['total_extensions'] == 2091
    grouped=defaultdict(Counter)
    sums=defaultdict(Counter)
    allcases=[]
    for case in make_cases():
        X,T=make_input(case['group'],case['n'],case['instance_seed'])
        f,fs=solve(X,T,False)
        b,bs=solve(X,T,True)
        assert f == b == case['expected_cardinality'],case
        fw,bw=operations(fs),operations(bs)
        outcome='win' if bw<fw else ('tie' if bw==fw else 'loss')
        grouped[case['group']][outcome]+=1
        grouped['TOTAL'][outcome]+=1
        for group in (case['group'],'TOTAL'):
            sums[group].update(forward_extensions=fw,bidirectional_extensions=bw,
                forward_layers=fs['forward_layers'],
                bidirectional_layers=bs['forward_layers']+bs['backward_layers'])
        allcases.append({**case,'forward':fs,'bidirectional':bs,'outcome':outcome})
    assert len(allcases) == 120
    assert grouped['TOTAL'] == {'tie': 67, 'loss': 53}
    assert sums['TOTAL']['forward_extensions'] == 6653
    assert sums['TOTAL']['bidirectional_extensions'] == 9528
    return {'exhaustive_cases_each_algorithm': checks, 'example': example,
            'cases': allcases, 'group_outcomes': dict(grouped),
            'group_totals': dict(sums)}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without Python -O: reproduction requires assertions.')
    print(json.dumps(run_checks(), indent=2))
