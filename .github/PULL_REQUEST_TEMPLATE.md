# Pull Request

## Summary

Describe the change briefly.

## Scope

- [ ] The change stays within CSV/XLSX table linting, schema templates, reports, or normalization.
- [ ] README claims match implemented behavior.
- [ ] New examples use synthetic data only.
- [ ] New issue codes are documented and tested.

## Checks

- [ ] `ruff format --check .`
- [ ] `ruff check .`
- [ ] `mypy src tests`
- [ ] `pytest`
- [ ] `python -m build`
- [ ] `python -m twine check dist/*`

## Privacy And Security

- [ ] No customer names, real lot numbers, internal material codes, or confidential measurements were added.
- [ ] No telemetry, upload, or network call was added by default.
