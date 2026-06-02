from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ColumnRule, Schema

BASIC_SCHEMA: dict[str, Any] = {
    "version": 1,
    "metadata": {"required": ["project", "operator", "date"]},
    "columns": {
        "sample_id": {
            "required": True,
            "aliases": ["試料ID", "サンプルID", "Sample ID", "sample id"],
            "type": "string",
            "unique": True,
        },
        "temperature": {
            "required": True,
            "aliases": ["温度", "熱処理温度", "temperature"],
            "unit": "degC",
            "accepted_units": ["℃", "C", "degC"],
            "type": "float",
            "range": [0, 2000],
        },
        "hold_time": {
            "aliases": ["保持時間", "時間", "hold time"],
            "unit": "min",
            "accepted_units": ["min", "分"],
            "type": "float",
            "nullable": True,
        },
        "tensile_strength": {
            "aliases": ["引張強さ", "引張強度", "tensile strength"],
            "unit": "MPa",
            "accepted_units": ["MPa"],
            "type": "float",
            "nullable": True,
        },
        "elongation": {
            "aliases": ["破断伸び", "伸び", "elongation"],
            "unit": "percent",
            "accepted_units": ["%", "percent"],
            "type": "float",
            "nullable": True,
        },
        "note": {
            "aliases": ["備考", "メモ", "note"],
            "type": "string",
            "nullable": True,
        },
    },
}


HEAT_TREATMENT_SCHEMA: dict[str, Any] = {
    "version": 1,
    "metadata": {"required": ["project", "operator", "date", "method"]},
    "columns": {
        "sample_id": {
            "required": True,
            "aliases": ["試料ID", "サンプルID", "Sample ID", "sample id"],
            "type": "string",
            "unique": True,
        },
        "material_grade": {
            "aliases": ["材質", "材料", "合金", "material", "material grade"],
            "type": "string",
            "nullable": True,
        },
        "lot_no": {
            "aliases": ["ロット", "ロット番号", "lot", "lot no"],
            "type": "string",
            "nullable": True,
        },
        "solution_temperature": {
            "required": True,
            "aliases": ["溶体化温度", "熱処理温度", "solution temperature"],
            "unit": "degC",
            "accepted_units": ["℃", "C", "degC"],
            "type": "float",
            "range": [0, 2000],
        },
        "hold_time": {
            "required": True,
            "aliases": ["保持時間", "時間", "hold time"],
            "unit": "min",
            "accepted_units": ["min", "分"],
            "type": "float",
            "range": [0, 10000],
        },
        "aging_temperature": {
            "aliases": ["時効温度", "aging temperature"],
            "unit": "degC",
            "accepted_units": ["℃", "C", "degC"],
            "type": "float",
            "nullable": True,
            "range": [0, 2000],
        },
        "cooling_condition": {
            "aliases": ["冷却条件", "冷却", "cooling condition"],
            "type": "string",
            "nullable": True,
        },
        "hardness": {
            "aliases": ["硬さ", "ビッカース硬さ", "hardness"],
            "unit": "HV",
            "accepted_units": ["HV", "Hv"],
            "type": "float",
            "nullable": True,
            "range": [0, 1000],
        },
        "note": {
            "aliases": ["備考", "メモ", "note"],
            "type": "string",
            "nullable": True,
        },
    },
}

TENSILE_TEST_SCHEMA: dict[str, Any] = {
    "version": 1,
    "metadata": {"required": ["project", "operator", "date", "test_method"]},
    "columns": {
        "sample_id": {
            "required": True,
            "aliases": ["試料ID", "サンプルID", "Sample ID", "sample id"],
            "type": "string",
            "unique": True,
        },
        "specimen_no": {
            "aliases": ["試験片No", "試験片番号", "specimen no"],
            "type": "string",
            "nullable": True,
        },
        "material_grade": {
            "aliases": ["材質", "材料", "合金", "material", "material grade"],
            "type": "string",
            "nullable": True,
        },
        "gauge_length": {
            "aliases": ["標点間距離", "ゲージ長", "gauge length"],
            "unit": "mm",
            "accepted_units": ["mm"],
            "type": "float",
            "nullable": True,
            "range": [0, 1000],
        },
        "yield_strength": {
            "aliases": ["降伏応力", "耐力", "yield strength"],
            "unit": "MPa",
            "accepted_units": ["MPa"],
            "type": "float",
            "nullable": True,
            "range": [0, 10000],
        },
        "tensile_strength": {
            "required": True,
            "aliases": ["引張強さ", "引張強度", "tensile strength"],
            "unit": "MPa",
            "accepted_units": ["MPa"],
            "type": "float",
            "range": [0, 10000],
        },
        "elongation": {
            "aliases": ["破断伸び", "伸び", "elongation"],
            "unit": "percent",
            "accepted_units": ["%", "percent"],
            "type": "float",
            "nullable": True,
            "range": [0, 1000],
        },
        "fracture_location": {
            "aliases": ["破断位置", "fracture location"],
            "type": "string",
            "nullable": True,
        },
        "note": {
            "aliases": ["備考", "メモ", "note"],
            "type": "string",
            "nullable": True,
        },
    },
}

SCHEMA_TEMPLATES: dict[str, dict[str, Any]] = {
    "basic": BASIC_SCHEMA,
    "heat-treatment": HEAT_TREATMENT_SCHEMA,
    "tensile-test": TENSILE_TEST_SCHEMA,
}


def write_schema_template(path: Path, template: str = "basic") -> None:
    try:
        schema = SCHEMA_TEMPLATES[template]
    except KeyError as exc:
        choices = ", ".join(sorted(SCHEMA_TEMPLATES))
        raise ValueError(f"unknown schema template: {template}. choices: {choices}") from exc
    path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_basic_schema(path: Path) -> None:
    write_schema_template(path, "basic")


def load_schema(path: Path) -> Schema:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("schema root must be an object")
    version = int(raw.get("version", 1))
    metadata = raw.get("metadata", {})
    required_metadata = tuple(str(item) for item in metadata.get("required", []))
    columns_raw = raw.get("columns")
    if not isinstance(columns_raw, dict) or not columns_raw:
        raise ValueError("schema must define non-empty columns")
    columns: list[ColumnRule] = []
    for name, config in columns_raw.items():
        if not isinstance(config, dict):
            raise ValueError(f"column rule must be an object: {name}")
        range_raw = config.get("range")
        range_min = None
        range_max = None
        if range_raw is not None:
            if (
                not isinstance(range_raw, list)
                or len(range_raw) != 2
                or not all(isinstance(item, int | float) for item in range_raw)
            ):
                raise ValueError(f"range must be [min, max] for column: {name}")
            range_min = float(range_raw[0])
            range_max = float(range_raw[1])
        columns.append(
            ColumnRule(
                name=str(name),
                required=bool(config.get("required", False)),
                aliases=tuple(str(item) for item in config.get("aliases", [])),
                value_type=str(config.get("type", "string")),
                unit=str(config["unit"]) if "unit" in config else None,
                accepted_units=tuple(str(item) for item in config.get("accepted_units", [])),
                nullable=bool(config.get("nullable", False)),
                unique=bool(config.get("unique", False)),
                range_min=range_min,
                range_max=range_max,
            )
        )
    return Schema(version=version, required_metadata=required_metadata, columns=tuple(columns))
