# v0.1.0 Release Notes

Initial MVP release of `materials-table-lint-jp`.

## Highlights

- Adds `mtlint` CLI for Japanese materials experiment CSV/XLSX table checks.
- Supports schema-based alias resolution, unit checks, required metadata, missing values, duplicate sample IDs, duplicate mapped column detection, numeric parsing, and simple range checks.
- Writes human-readable summaries, JSON reports, and normalized CSV for inputs without errors.
- Uses Python standard library for CSV/JSON behavior.
- Keeps `.xlsx` support optional through `openpyxl`.

## Verification

- `ruff format --check .`
- `ruff check .`
- `mypy src tests`
- `pytest`
- `python -m build`
- `python -m twine check dist/*`

## Notes

This is a new project. It does not yet have public adoption metrics, stars, downloads, or external usage examples.
