from pathlib import Path

from materials_table_lint_jp.analyzer import analyze, split_column_unit
from materials_table_lint_jp.reader import read_table
from materials_table_lint_jp.schema import load_schema


def write_schema(tmp_path: Path) -> Path:
    schema = tmp_path / "schema.json"
    schema.write_text(
        """
{
  "version": 1,
  "metadata": {"required": ["project", "operator", "date"]},
  "columns": {
    "sample_id": {
      "required": true,
      "aliases": ["試料ID", "サンプルID"],
      "type": "string",
      "unique": true
    },
    "temperature": {
      "required": true,
      "aliases": ["温度"],
      "unit": "degC",
      "accepted_units": ["℃", "C", "degC"],
      "type": "float",
      "range": [0, 2000]
    },
    "hold_time": {
      "aliases": ["保持時間"],
      "unit": "min",
      "accepted_units": ["min"],
      "type": "float",
      "nullable": true
    }
  }
}
""".strip(),
        encoding="utf-8",
    )
    return schema


def test_split_column_unit() -> None:
    assert split_column_unit("温度[℃]") == ("温度", "℃")
    assert split_column_unit("引張強さ(MPa)") == ("引張強さ", "MPa")
    assert split_column_unit("試料ID") == ("試料ID", None)


def test_analyze_detects_duplicate_and_missing_values(tmp_path: Path) -> None:
    data = tmp_path / "data.csv"
    data.write_text(
        "\n".join(
            [
                "# project=Demo",
                "# operator=Tanaka",
                "# date=2026-06-01",
                "試料ID,温度[℃],保持時間[min]",
                "A-001,520,60",
                "A-002,520,",
                "A-002,540,30",
            ]
        ),
        encoding="utf-8",
    )

    analysis = analyze(read_table(data), load_schema(write_schema(tmp_path)))
    codes = [issue.code for issue in analysis.issues]

    assert "DUPLICATE_SAMPLE_ID" in codes
    assert "MISSING_VALUE" not in codes
    assert analysis.matches["temperature"].output == "temperature_degC"
    assert analysis.normalized_rows[0]["sample_id"] == "A-001"


def test_required_metadata_and_range_errors(tmp_path: Path) -> None:
    data = tmp_path / "data.csv"
    data.write_text("試料ID,温度[℃]\nA-001,2500\n", encoding="utf-8")

    analysis = analyze(read_table(data), load_schema(write_schema(tmp_path)))
    codes = [issue.code for issue in analysis.issues]

    assert codes.count("MISSING_METADATA") == 3
    assert "RANGE_VIOLATION" in codes
    assert analysis.status == "error"


def test_numeric_parse_error(tmp_path: Path) -> None:
    data = tmp_path / "data.csv"
    data.write_text(
        "# project=Demo\n# operator=Tanaka\n# date=2026-06-01\n試料ID,温度[℃]\nA-001,high\n",
        encoding="utf-8",
    )

    analysis = analyze(read_table(data), load_schema(write_schema(tmp_path)))

    assert any(issue.code == "NUMERIC_PARSE_ERROR" for issue in analysis.issues)
