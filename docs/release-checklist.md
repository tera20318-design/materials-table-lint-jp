# Release Checklist

Use this checklist before tagging a release. It is intentionally small so that releases stay reproducible.

## Before Tagging

- Confirm `pyproject.toml` and `src/materials_table_lint_jp/__init__.py` use the same version.
- Update `CHANGELOG.md`.
- Add or update `docs/release-notes-vX.Y.Z.md`.
- Confirm README only documents commands and behavior that work locally.
- Confirm examples are synthetic and do not include customer names, lot numbers, or proprietary material codes.

## Local Verification

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
python -m build
python -m twine check dist/*
```

## PyPI Preparation

The project is not on PyPI yet. Before claiming PyPI availability:

- Confirm the package name is available.
- Prefer PyPI trusted publishing from GitHub Actions once the repository is ready.
- Test the upload path with TestPyPI first.
- Install the published package in a clean environment and verify `mtlint --version`.
- Update README installation instructions only after the package is actually published.
