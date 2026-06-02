# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-06-02

### Added

- `mtlint init --template` with `basic`, `heat-treatment`, and `tensile-test` schema templates.
- Synthetic heat treatment and tensile test CSV/schema examples.
- README positioning note to clarify that this CLI complements, rather than replaces, analysis libraries and generic validation frameworks.

## [0.1.0] - 2026-06-02

### Added

- Initial `mtlint` CLI.
- CSV input with `# key=value` metadata comments.
- Optional `.xlsx` input through `openpyxl`.
- JSON schema-based column aliases, unit checks, required metadata, uniqueness, duplicate mapped column detection, numeric parsing, and range checks.
- `init`, `inspect`, `lint`, and `normalize` commands.
- Human-readable CLI summaries, JSON reports, and normalized CSV output for inputs without errors.
- Tests, GitHub Actions CI, examples, and OSS documentation.
