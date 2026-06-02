# Comparison And Positioning

`materials-table-lint-jp` is intentionally small. It checks Japanese materials
experiment tables before analysis or sharing.

## Where It Fits

Use this project when you have simple CSV/XLSX tables and want to catch:

- Japanese/English column-name drift.
- Missing metadata such as project, operator, and date.
- Missing or mismatched unit notation in column names.
- Duplicate sample IDs.
- Missing required values.
- Numeric parse errors and simple out-of-range values.

## What It Is Not

This project is not a replacement for:

- `pandas`, R, or other data analysis tools.
- `pandera`, Great Expectations, or other broad validation frameworks.
- `pymatgen`, `matminer`, NOMAD, or materials databases.
- ELN/LIMS systems.
- OCR/PDF extraction.
- Regulated quality assurance or standards-compliance decisions.

## Why A Small CLI Can Still Help

Many materials experiment records start as Excel or CSV tables. A small local CLI
can provide a repeatable first check before those tables enter notebooks, scripts,
or shared folders. The goal is not to infer scientific meaning. The goal is to make
the table shape explicit and testable.

## Current Limits

- Schema files are JSON only.
- Unit conversion is not implemented.
- XLSX support is limited to simple tabular sheets.
- Examples are synthetic and do not represent adoption or production usage.
