"""Tests for FusionGDB2 parsing behavior."""

import sys
from pathlib import Path

import pytest

from fusion_report.createdb import CreateDB
import fusion_report.createdb as createdb_module


pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 12), reason="fusion-report requires Python >= 3.12"
)


def test_build_fusiongdb2_parses_txt_to_expected_fusion_pairs(tmp_path: Path, monkeypatch) -> None:
    """Verify FusionGDB2 TXT rows are parsed into correct fusion-pair CSV values.

    The parser is expected to read a 6-column, headerless TSV and construct
    fusion pairs from 0-based columns 2 (5-prime gene) and 4 (3-prime gene).
    """
    sample_txt = tmp_path / "fusiongdb2_sample.txt"
    sample_txt.write_text(
        "rowA\tidA\tBCR\tidB\tABL1\textra\n"
        "rowB\tidC\tEML4\tidD\tALK\textra\n",
        encoding="utf-8",
    )

    captured: dict[str, object] = {}

    class DummyFusionGDB2:
        """Test double capturing database setup inputs."""

        def __init__(self, path: str) -> None:
            captured["path"] = path

        def setup(self, files, delimiter=",", skip_header=False) -> None:
            captured["files"] = files
            captured["delimiter"] = delimiter
            captured["skip_header"] = skip_header

        def insert_hgnc_pairs(self, pairs) -> None:
            captured["hgnc_pairs"] = pairs

    class DummyResolver:
        """Simple resolver returning deterministic HGNC IDs for test genes."""

        @staticmethod
        def resolve_with_metadata(symbol, chromosome_hint=None, ensembl_id=None, entrez_id=None):
            return {
                "input_symbol": symbol,
                "resolved_symbol": symbol,
                "hgnc_id": f"HGNC:{symbol}",
                "resolved_via_alias": False,
                "known": True,
                "ambiguous": False,
                "chromosome_matched": False,
                "ensembl_matched": False,
                "entrez_matched": bool(entrez_id),
            }

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(createdb_module, "FusionGDB2", DummyFusionGDB2)

    errors: list[str] = []
    CreateDB.build_fusiongdb2(str(sample_txt), errors, DummyResolver())

    assert errors == []
    assert captured["path"] == "."
    assert captured["files"] == ["fusionGDB2.csv"]
    assert captured["delimiter"] == ","
    assert captured["skip_header"] is False
    assert len(captured["hgnc_pairs"]) == 2
    assert captured["hgnc_pairs"][0] == ("HGNC:BCR", "HGNC:ABL1", "BCR--ABL1")
    assert captured["hgnc_pairs"][1] == ("HGNC:EML4", "HGNC:ALK", "EML4--ALK")

    generated_csv = tmp_path / "fusionGDB2.csv"
    assert generated_csv.exists()
    assert generated_csv.read_text(encoding="utf-8").splitlines() == [
        "BCR--ABL1",
        "EML4--ALK",
    ]
