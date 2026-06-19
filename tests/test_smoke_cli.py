import os
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "bin" / "fusion_report"


pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 12), reason="fusion-report requires Python >= 3.12"
)


def run_cli(*args: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(REPO_ROOT),
        check=False,
    )


def test_cli_help_top_level() -> None:
    result = run_cli("--help")
    assert result.returncode == 0, result.stderr
    assert "{run,download,createdb}" in result.stdout


def test_cli_help_run() -> None:
    result = run_cli("run", "--help")
    assert result.returncode == 0, result.stderr
    assert "usage: fusion_report run" in result.stdout


def test_cli_help_download() -> None:
    result = run_cli("download", "--help")
    assert result.returncode == 0, result.stderr
    assert "usage: fusion_report download" in result.stdout


def test_cli_help_createdb() -> None:
    result = run_cli("createdb", "--help")
    assert result.returncode == 0, result.stderr
    assert "usage: fusion_report createdb" in result.stdout
