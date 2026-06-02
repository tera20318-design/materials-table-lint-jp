# Review Log

This file records pre-application review work for the initial public repository.

## 2026-06-02

### Theme Selection

The selected B+D direction combines:

- Materials experiment Excel/CSV normalization and linting.
- Materials experiment metadata templates and validation.

This was chosen because it is more directly useful for materials-technology work than a general AI/CLI environment doctor, while still being small enough for a weekend MVP.

### Scope Guardrails

- Use explicit schemas and dictionaries instead of automatic scientific inference.
- Keep `.xlsx` optional.
- Avoid OCR, PDF extraction, LLM extraction, ELN/LIMS replacement, and regulated QA claims.
- Use only synthetic example data.
