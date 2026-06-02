import json
from pathlib import Path

from materials_table_lint_jp.schema import (
    SCHEMA_TEMPLATES,
    load_schema,
    write_basic_schema,
    write_schema_template,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_write_and_load_basic_schema(tmp_path: Path) -> None:
    path = tmp_path / "schema.json"
    write_basic_schema(path)

    schema = load_schema(path)

    assert schema.version == 1
    assert "project" in schema.required_metadata
    assert schema.columns[0].name == "sample_id"
    assert schema.columns[0].unique is True


def test_material_schema_templates_load(tmp_path: Path) -> None:
    for template in SCHEMA_TEMPLATES:
        path = tmp_path / f"{template}.json"
        write_schema_template(path, template)

        schema = load_schema(path)

        assert schema.version == 1
        assert schema.columns[0].name == "sample_id"


def test_unknown_schema_template_raises(tmp_path: Path) -> None:
    path = tmp_path / "schema.json"

    try:
        write_schema_template(path, "missing-template")
    except ValueError as exc:
        assert "unknown schema template" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_example_schemas_match_built_in_templates() -> None:
    examples = REPO_ROOT / "examples"

    assert (
        json.loads((examples / "basic.schema.json").read_text(encoding="utf-8"))
        == SCHEMA_TEMPLATES["basic"]
    )
    assert (
        json.loads((examples / "heat_treatment.schema.json").read_text(encoding="utf-8"))
        == SCHEMA_TEMPLATES["heat-treatment"]
    )
    assert (
        json.loads((examples / "tensile_test.schema.json").read_text(encoding="utf-8"))
        == SCHEMA_TEMPLATES["tensile-test"]
    )
