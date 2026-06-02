# Codex Maintenance Plan

This document explains how Codex or API credits would be used for maintaining this
repository. It is not a runtime feature claim.

## Current Runtime

- `materials-table-lint-jp` does not call the OpenAI API.
- The CLI has no telemetry and no network calls by default.
- User CSV/XLSX files stay local unless the user explicitly shares them elsewhere.

## Useful Maintainer Workflows

Credits or Codex access would be useful for:

- Drafting and reviewing small pull requests for schema-template improvements.
- Turning reported CSV/XLSX edge cases into focused tests.
- Reviewing README, release notes, and security wording for overclaims.
- Drafting issue triage responses without exposing private experiment data.
- Checking whether proposed examples are synthetic and do not contain customer,
  lot, material, equipment, or internal project identifiers.

## Guardrails

- Do not add hidden OpenAI API calls to the CLI.
- Do not upload real experiment data, customer names, lot numbers, or internal
  material codes for triage.
- Do not claim stars, downloads, users, or external adoption unless those facts are
  public and verifiable.
- Do not describe generated suggestions as scientific validation.
- Keep AI-assisted changes reviewable through tests, CI, and release notes.

## Good First Maintenance Tasks

- Add XRD and coating-test schema templates using synthetic examples.
- Add focused tests for Windows path handling and Japanese column aliases.
- Add a PyPI publishing workflow only after trusted publishing is configured.
- Add more docs for users who normalize tables before pandas/R analysis.
