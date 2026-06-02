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


def write_basic_schema(path: Path) -> None:
    path.write_text(json.dumps(BASIC_SCHEMA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
