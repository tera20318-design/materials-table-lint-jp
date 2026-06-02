# Review Log

This file records pre-application review work for the initial public repository.

## 2026-06-02

### Theme Selection

The selected B+D direction combines:

- Materials experiment Excel/CSV normalization and linting.
- Materials experiment metadata templates and validation.

This was chosen because it is more directly useful for materials-technology work than a general AI/CLI environment doctor, while still being small enough for a small initial release.

### Scope Guardrails

- Use explicit schemas and dictionaries instead of automatic scientific inference.
- Keep `.xlsx` optional.
- Avoid OCR, PDF extraction, LLM extraction, ELN/LIMS replacement, and regulated QA claims.
- Use only synthetic example data.

### Pre-Application Fixes

- Fixed Windows CLI output so Japanese column names do not fail on non-UTF-8 consoles.
- Added an error for duplicate input columns that map to the same schema column.
- Made missing `.xlsx` sheets return a clear CLI error.
- Made `normalize` skip normalized CSV output when the analysis has errors; JSON reports can still be written.
- Verified GitHub Actions CI on Ubuntu and Windows with Python 3.11 and 3.12.
