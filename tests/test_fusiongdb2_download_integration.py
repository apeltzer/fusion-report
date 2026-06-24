"""Integration test for live FusionGDB2 download."""

import os
import sys
import warnings

import pytest
from urllib3.exceptions import InsecureRequestWarning

from fusion_report.common.exceptions.download import DownloadException
from fusion_report.common.net import Net
from fusion_report.settings import Settings


pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 12) or os.getenv("RUN_LIVE_NETWORK_TESTS") != "1",
    reason=(
        "fusion-report requires Python >= 3.12 and RUN_LIVE_NETWORK_TESTS=1 "
        "for live network tests"
    ),
)


def test_download_fusiongdb2_live(tmp_path, monkeypatch) -> None:
    """Download live FusionGDB2 data and validate basic structure.

    The downloaded file is expected to be a tab-separated file with at least
    6 columns, where column indices 2 and 4 contain gene symbols used to
    construct fusion pairs.
    """
    monkeypatch.chdir(tmp_path)

    url = f"{Settings.FUSIONGDB2['HOSTNAME']}/{Settings.FUSIONGDB2['FILE']}"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            Net.get_large_file(url, no_ssl=True)
    except DownloadException as ex:
        pytest.skip(f"Live FusionGDB2 download unavailable in this environment: {ex}")

    downloaded_file = tmp_path / Settings.FUSIONGDB2["FILE"]
    assert downloaded_file.exists()
    assert downloaded_file.stat().st_size > 1024

    first_non_empty_line = ""
    with open(downloaded_file, "r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.strip():
                first_non_empty_line = line.strip()
                break

    assert first_non_empty_line
    columns = first_non_empty_line.split("\t")
    assert len(columns) >= 6
    assert columns[2].strip() != ""
    assert columns[4].strip() != ""
