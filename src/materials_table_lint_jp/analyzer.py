from __future__ import annotations

import re
from collections import defaultdict

from .models import Analysis, ColumnMatch, ColumnRule, Issue, Schema, Severity, Table

_UNIT_PATTERN = re.compile(
    r"^(?P<label>.+?)[\s_]*(?:\[(?P<bracket>[^\]]+)\]|\((?P<paren>[^)]+)\))$"
)


def normalize_label(value: str) -> str:
    return re.sub(r"[\s_\-]+", "", value.strip().casefold())


def split_column_unit(header: str) -> tuple[str, str | None]:
    stripped = header.strip()
    match = _UNIT_PATTERN.match(stripped)
    if not match:
        return stripped, None
    label = match.group("label").strip()
    unit = (match.group("bracket") or match.group("paren") or "").strip()
    return label, unit or None


def analyze(table: Table, schema: Schema) -> Analysis:
    analysis = Analysis(table=table, schema=schema)
    match_columns(analysis)
    check_metadata(analysis)
    check_unknown_columns(analysis)
    check_required_columns(analysis)
    normalize_rows(analysis)
    check_values(analysis)
    check_uniqueness(analysis)
    return analysis


def match_columns(analysis: Analysis) -> None:
    alias_map: dict[str, ColumnRule] = {}
    for rule in analysis.schema.columns:
        for alias in (rule.name, *rule.aliases):
            alias_map[normalize_label(alias)] = rule

    for source in analysis.table.headers:
        label, unit = split_column_unit(source)
        matched_rule = alias_map.get(normalize_label(label))
        if matched_rule is None:
            continue
        analysis.matches[matched_rule.name] = ColumnMatch(
            source=source,
            normalized=matched_rule.name,
            output=matched_rule.output_name,
            unit=unit,
            rule=matched_rule,
        )
        if (
            matched_rule.accepted_units
            and unit is not None
            and unit not in matched_rule.accepted_units
        ):
            analysis.issues.append(
                Issue(
                    code="UNIT_MISMATCH",
                    severity=Severity.WARNING,
                    message=(
                        f"Column '{source}' uses unit '{unit}', expected one of "
                        f"{', '.join(matched_rule.accepted_units)}."
                    ),
                    column=matched_rule.name,
                    value=unit,
                )
            )
        if matched_rule.accepted_units and unit is None:
            analysis.issues.append(
                Issue(
                    code="MISSING_UNIT",
                    severity=Severity.WARNING,
                    message=f"Column '{source}' has no unit notation.",
                    column=matched_rule.name,
                )
            )


def check_metadata(analysis: Analysis) -> None:
    for key in analysis.schema.required_metadata:
        if not analysis.table.metadata.get(key):
            analysis.issues.append(
                Issue(
                    code="MISSING_METADATA",
                    severity=Severity.ERROR,
                    message=f"Required metadata is missing: {key}",
                    value=key,
                )
            )


def check_unknown_columns(analysis: Analysis) -> None:
    known_sources = {match.source for match in analysis.matches.values()}
    for header in analysis.table.headers:
        if header not in known_sources:
            analysis.issues.append(
                Issue(
                    code="UNKNOWN_COLUMN",
                    severity=Severity.WARNING,
                    message=f"Column is not mapped by schema aliases: {header}",
                    value=header,
                )
            )


def check_required_columns(analysis: Analysis) -> None:
    for rule in analysis.schema.columns:
        if rule.required and rule.name not in analysis.matches:
            analysis.issues.append(
                Issue(
                    code="MISSING_REQUIRED_COLUMN",
                    severity=Severity.ERROR,
                    message=f"Required column is missing: {rule.name}",
                    column=rule.name,
                )
            )


def normalize_rows(analysis: Analysis) -> None:
    ordered_matches = [
        match for rule in analysis.schema.columns if (match := analysis.matches.get(rule.name))
    ]
    for row in analysis.table.rows:
        normalized: dict[str, str] = {}
        for match in ordered_matches:
            normalized[match.output] = row.get(match.source, "")
        analysis.normalized_rows.append(normalized)


def check_values(analysis: Analysis) -> None:
    for row_index, normalized in enumerate(
        analysis.normalized_rows,
        start=2 + len(analysis.table.metadata),
    ):
        for match in analysis.matches.values():
            value = normalized.get(match.output, "").strip()
            rule = match.rule
            if not value:
                if rule.required and not rule.nullable:
                    analysis.issues.append(
                        Issue(
                            code="MISSING_VALUE",
                            severity=Severity.ERROR,
                            message=f"Required value is missing for column: {rule.name}",
                            column=rule.name,
                            row=row_index,
                        )
                    )
                continue
            if rule.value_type == "float":
                try:
                    number = float(value)
                except ValueError:
                    analysis.issues.append(
                        Issue(
                            code="NUMERIC_PARSE_ERROR",
                            severity=Severity.ERROR,
                            message=f"Value is not numeric for column: {rule.name}",
                            column=rule.name,
                            row=row_index,
                            value=value,
                        )
                    )
                    continue
                if rule.range_min is not None and number < rule.range_min:
                    analysis.issues.append(range_issue(rule, row_index, value))
                if rule.range_max is not None and number > rule.range_max:
                    analysis.issues.append(range_issue(rule, row_index, value))


def range_issue(rule: ColumnRule, row_index: int, value: str) -> Issue:
    return Issue(
        code="RANGE_VIOLATION",
        severity=Severity.ERROR,
        message=f"Value is outside range for column: {rule.name}",
        column=rule.name,
        row=row_index,
        value=value,
    )


def check_uniqueness(analysis: Analysis) -> None:
    for match in analysis.matches.values():
        if not match.rule.unique:
            continue
        seen: defaultdict[str, list[int]] = defaultdict(list)
        for row_index, normalized in enumerate(
            analysis.normalized_rows,
            start=2 + len(analysis.table.metadata),
        ):
            value = normalized.get(match.output, "").strip()
            if value:
                seen[value].append(row_index)
        for value, rows in seen.items():
            if len(rows) > 1:
                for row in rows[1:]:
                    analysis.issues.append(
                        Issue(
                            code="DUPLICATE_SAMPLE_ID",
                            severity=Severity.ERROR,
                            message=f"Duplicate value in unique column: {match.rule.name}",
                            column=match.rule.name,
                            row=row,
                            value=value,
                        )
                    )
