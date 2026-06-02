# AGENTS.md

## Project Purpose

`materials-table-lint-jp` is a small OSS CLI for Japanese materials experiment tables.
It checks CSV/XLSX tables for column-name drift, unit notation, required metadata,
missing values, sample ID duplication, numeric parsing, and simple range rules. It can
also write normalized CSV and JSON reports.

The project is not a generic materials database, ELN, LIMS, OCR system, or AI extraction
tool. Keep the scope narrow and practical.

## Users

- Japanese materials engineers and researchers who keep experiment data in Excel/CSV.
- Individual developers preparing materials experiment data for Python/R analysis.
- Maintainers who need a small, inspectable lint step before sharing or reusing tables.

## Directory Structure

- `src/materials_table_lint_jp/`: package source.
- `tests/`: pytest tests.
- `examples/`: sample CSV, schema, normalized output, and reports.
- `docs/`: roadmap, release notes, application draft, and review notes.
- `.github/`: CI and issue templates.

## Implementation Policy

- Prefer Python standard library for core CSV/JSON behavior.
- Keep `.xlsx` support optional through `openpyxl`; do not require it for CSV use.
- Use explicit JSON schema files for MVP. YAML support is out of scope until requested.
- Keep built-in schema templates small and tied to synthetic examples that lint cleanly.
- Keep lint issue codes stable and documented.
- Do not silently infer scientific meaning. Use schema aliases, units, and range rules.
- Do not include proprietary standards text, real customer data, or confidential examples.

## Test Policy

Tests should cover:

- Japanese alias resolution.
- Unit parsing from column names such as `温度[℃]`.
- Required metadata and required column failures.
- Duplicate and blank sample IDs.
- Nullable vs non-nullable numeric values.
- Numeric parse errors and range checks.
- Normalized CSV column order.
- JSON report shape and stable issue codes.
- Optional `.xlsx` behavior when `openpyxl` is unavailable.

## Commands

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src tests
pytest
python -m build
python -m twine check dist/*
```

For optional Excel support:

```bash
python -m pip install -e ".[dev,xlsx]"
```

## README Requirements

README must include:

- Honest project status: new repo, no adoption metrics unless true.
- What the MVP supports and does not support.
- Quick start using `examples/sample.csv` and `examples/basic.schema.json`.
- Built-in template examples for currently implemented `mtlint init --template` choices.
- `mtlint init`, `inspect`, `lint`, and `normalize` examples.
- Privacy/security notes for local experiment data.
- Optional Excel dependency instructions.
- Stable issue-code list or a pointer to docs.

## PR Checklist

- [ ] Tests pass.
- [ ] Lint/typecheck/build pass.
- [ ] README only claims implemented behavior.
- [ ] Sample data is synthetic and non-confidential.
- [ ] New issue codes are documented and tested.
- [ ] No broad scope creep into ELN/LIMS/OCR/AI extraction.

## Security And Privacy

- This CLI reads local files and writes local reports only.
- Do not add telemetry, external uploads, or network calls by default.
- Do not include real experiment data, customer names, lot numbers, or internal material
  codes in tests or examples.
- Warn users to review normalized outputs before sharing.
- If future auto-fix behavior is added, it must be explicit and opt-in.

## Do Not

- Do not fabricate GitHub stars, downloads, users, or adoption.
- Do not present the repo as more mature than it is.
- Do not add unnecessary dependencies.
- Do not claim PyPI publication until it exists.
- Do not claim support for arbitrary Excel layouts, OCR, PDF extraction, JIS standard
  compliance, or regulated quality decisions.
- Do not write README examples for non-working commands.
