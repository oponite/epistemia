"""Count-only benchmark dispatch, accounting, and reporting checks."""

import pytest

from benchmark_cardinality import make_cases, measure_worker, run_worker, validate_records
from benchmark_layers import METHODS, write_report


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('values,target,count', [([1,6,11,16,21,26],34,4), ([2,4,6],9,None)])
def test_count_only_worker(method, values, target, count):
    result = run_worker(measure_worker, (method, values, target, count, None))
    assert result['status'] == 'COMPLETE', result['error']
    assert len(result['measurements']) == 5
    assert all(r['seconds'] > 0 and r['calls'] >= 1 for r in result['measurements'])


def test_count_accounting_report_and_preservation(tmp_path):
    cases = make_cases()
    rows, ledger = [], []
    for case in cases:
        for method, seconds in zip(METHODS, (.002, .004, .006, .001)):
            common = {**case, 'method': method}
            ledger.append({**common, 'status':'COMPLETE', 'calibration':'', 'error':''})
            rows.extend({**common, 'repeat': r, 'calls':8, 'seconds':seconds} for r in range(5))
    assert len(rows) == 2400 and len(ledger) == 480
    validate_records(rows, ledger, cases, METHODS)
    metadata = dict(run_id='fixture', python='test', numpy='test', matplotlib='test', platform='test')
    report = tmp_path/'REPORT.md'
    write_report(rows, ledger, cases, metadata, report, 1.)
    text = report.read_text()
    assert '| 8 | 1 | 2.000000 | 4.000000 | 6.000000 | 1.000000 | 2 (5) | 4 (5) | 6 (5) |' in text
    assert '2400 timing rows, 480 jobs' in text
    with pytest.raises(FileExistsError):
        write_report(rows, ledger, cases, metadata, report, 1.)
    assert report.read_text() == text
    job = ledger[0]
    job['status'] = 'TIMEOUT'
    rows = [r for r in rows if any(r[f] != job[f] for f in ('group','n','instance','method'))]
    validate_records(rows, ledger, cases, METHODS)
    write_report(rows, ledger, cases, metadata, tmp_path/'timeout.md', 1.)
    assert 'Incomplete group' in (tmp_path/'timeout.md').read_text()
    with pytest.raises(AssertionError):
        validate_records(rows+[dict(rows[0])], ledger, cases, METHODS)
