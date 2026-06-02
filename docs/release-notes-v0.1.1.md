# v0.1.1 Release Notes

Small follow-up release focused on materials-specific examples.

## Highlights

- Adds `mtlint init --template heat-treatment`.
- Adds `mtlint init --template tensile-test`.
- Adds synthetic heat treatment and tensile test CSV/schema examples under `examples/`.
- Updates README wording to clarify the project positioning without claiming adoption or broader scientific validation.

## Verification

Passed locally on 2026-06-02:

- `ruff format --check .`
- `ruff check .`
- `mypy src tests`
- `pytest`
- `python -m build`
- `python -m twine check dist/*`

## Notes

This is still a new project. It does not yet have public adoption metrics, downloads, or external usage examples.
