from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .models import Analysis


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def write_normalized_csv(path: Path, analysis: Analysis) -> None:
    if not analysis.normalized_rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(analysis.normalized_rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(analysis.normalized_rows)


def render_summary(analysis: Analysis) -> str:
    error_count = sum(1 for issue in analysis.issues if issue.severity.value == "error")
    warning_count = sum(1 for issue in analysis.issues if issue.severity.value == "warning")
    lines = [
        "Materials Table Lint JP",
        f"Input: {analysis.table.path}",
        f"Rows: {len(analysis.table.rows)}",
        f"Status: {analysis.status} (errors={error_count}, warnings={warning_count})",
        "",
        "Mapped columns:",
    ]
    if analysis.matches:
        for match in analysis.matches.values():
            unit = f" unit={match.unit}" if match.unit else ""
            lines.append(f"  - {match.source} -> {match.output}{unit}")
    else:
        lines.append("  - none")
    if analysis.issues:
        lines.extend(["", "Issues:"])
        for issue in analysis.issues:
            location = ""
            if issue.row is not None:
                location += f" row={issue.row}"
            if issue.column is not None:
                location += f" column={issue.column}"
            lines.append(f"  [{issue.severity.value}] {issue.code}{location}: {issue.message}")
    return "\n".join(lines).rstrip() + "\n"
