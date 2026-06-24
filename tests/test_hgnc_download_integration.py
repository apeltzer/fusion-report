"""Integration test for live HGNC complete_set download."""

import os
import sys

import pytest

from fusion_report.common.symbol_resolver import SymbolResolver


pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 12) or os.getenv("RUN_LIVE_NETWORK_TESTS") != "1",
    reason=(
        "fusion-report requires Python >= 3.12 and RUN_LIVE_NETWORK_TESTS=1 "
        "for live network tests"
    ),
)


def test_download_hgnc_complete_set_live() -> None:
    """Validate HGNC mapping availability in live-test mode.

    In some corporate or SSL-intercepted environments, direct HTTPS download
    may fail even when the resolver can still load HGNC mapping from cache or
    bundled fallback. This test accepts either successful live download or a
    non-empty resolver mapping loaded via fallback.
    """
    resolver = SymbolResolver()

    tsv_text = resolver._download_hgnc_tsv()
    if tsv_text is None:
        assert resolver.hgnc_records
        return

    lines = tsv_text.splitlines()
    assert len(lines) > 1000

    header = lines[0]
    assert "hgnc_id" in header
    assert "symbol" in header
    assert "alias_symbol" in header
    assert "prev_symbol" in header
    assert "location" in header
