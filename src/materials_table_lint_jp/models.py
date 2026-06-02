from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Issue:
    code: str
    severity: Severity
    message: str
    column: str | None = None
    row: int | None = None
    value: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
        }
        if self.column is not None:
            payload["column"] = self.column
        if self.row is not None:
            payload["row"] = self.row
        if self.value is not None:
            payload["value"] = self.value
        return payload


@dataclass(frozen=True)
class ColumnRule:
    name: str
    required: bool = False
    aliases: tuple[str, ...] = ()
    value_type: str = "string"
    unit: str | None = None
    accepted_units: tuple[str, ...] = ()
    nullable: bool = False
    unique: bool = False
    range_min: float | None = None
    range_max: float | None = None

    @property
    def output_name(self) -> str:
        if self.unit:
            suffix = (
                self.unit.replace("℃", "degC")
                .replace("%", "percent")
                .replace("/", "_per_")
                .replace(" ", "_")
            )
            return f"{self.name}_{suffix}"
        return self.name


@dataclass(frozen=True)
class Schema:
    version: int
    required_metadata: tuple[str, ...]
    columns: tuple[ColumnRule, ...]


@dataclass(frozen=True)
class Table:
    path: Path
    metadata: dict[str, str]
    headers: tuple[str, ...]
    rows: tuple[dict[str, str], ...]


@dataclass(frozen=True)
class ColumnMatch:
    source: str
    normalized: str
    output: str
    unit: str | None
    rule: ColumnRule


@dataclass
class Analysis:
    table: Table
    schema: Schema
    issues: list[Issue] = field(default_factory=list)
    matches: dict[str, ColumnMatch] = field(default_factory=dict)
    normalized_rows: list[dict[str, str]] = field(default_factory=list)

    @property
    def status(self) -> str:
        if any(issue.severity == Severity.ERROR for issue in self.issues):
            return "error"
        if self.issues:
            return "warning"
        return "ok"

    def to_report(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "input": str(self.table.path),
            "rows": len(self.table.rows),
            "metadata": dict(self.table.metadata),
            "issues": [issue.to_dict() for issue in self.issues],
            "normalized_columns": {match.source: match.output for match in self.matches.values()},
        }
