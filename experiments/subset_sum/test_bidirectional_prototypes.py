"""Reproduce the published operation counts and exhaustive correctness checks."""

import json
from pathlib import Path

from bidirectional_prototypes import run_checks


def test_published_bidirectional_report():
    report = Path(__file__).with_name('bidirectional') / 'results.json'
    assert run_checks() == json.loads(report.read_text())
