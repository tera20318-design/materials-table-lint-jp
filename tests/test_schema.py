from pathlib import Path

from materials_table_lint_jp.schema import load_schema, write_basic_schema


def test_write_and_load_basic_schema(tmp_path: Path) -> None:
    path = tmp_path / "schema.json"
    write_basic_schema(path)

    schema = load_schema(path)

    assert schema.version == 1
    assert "project" in schema.required_metadata
    assert schema.columns[0].name == "sample_id"
    assert schema.columns[0].unique is True
