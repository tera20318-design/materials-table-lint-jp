from pathlib import Path
from typing import Any

import pytest

from materials_table_lint_jp.reader import read_table


def test_read_csv_metadata_and_rows(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("# project=Demo\n試料ID,温度[℃]\nA-001,500\n", encoding="utf-8")

    table = read_table(path)

    assert table.metadata == {"project": "Demo"}
    assert table.headers == ("試料ID", "温度[℃]")
    assert table.rows[0]["試料ID"] == "A-001"


def test_xlsx_without_openpyxl_has_clear_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "data.xlsx"
    path.write_bytes(b"not a real workbook")
    import builtins

    original_import = builtins.__import__

    def fake_import(name: str, *args: Any, **kwargs: Any) -> object:
        if name == "openpyxl":
            raise ImportError("blocked")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match="Excel input requires optional dependency"):
        read_table(path)


def test_read_xlsx_with_openpyxl(tmp_path: Path) -> None:
    pytest.importorskip("openpyxl")
    from openpyxl import Workbook

    path = tmp_path / "data.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["# project=Demo"])
    sheet.append(["試料ID", "温度[℃]"])
    sheet.append(["A-001", 500])
    workbook.save(path)

    table = read_table(path)

    assert table.metadata == {"project": "Demo"}
    assert table.headers == ("試料ID", "温度[℃]")
    assert table.rows[0]["温度[℃]"] == "500"
