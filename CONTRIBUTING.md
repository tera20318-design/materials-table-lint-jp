# Contributing

Thanks for considering a contribution.

## Scope

This project focuses on small, inspectable checks for Japanese materials experiment
tables. Keep contributions close to CSV/XLSX table linting, metadata templates,
unit/column dictionaries, and normalized CSV/JSON output.

Out of scope for now:

- Generic ELN/LIMS features.
- PDF/OCR/LLM extraction.
- Quality assurance pass/fail decisions.
- Proprietary standards text or confidential sample data.

## Development

```bash
python -m pip install -e ".[dev,xlsx]"
ruff format --check .
ruff check .
mypy src tests
pytest
python -m build
python -m twine check dist/*
```

## Sample Data

Only use synthetic data in examples and tests. Do not include customer names,
real lot numbers, internal material codes, or unpublished experiment results.
