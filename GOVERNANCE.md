# Governance

`materials-table-lint-jp` is currently a small maintainer-led project.

## Maintainer Responsibilities

Maintainers are responsible for:

- Keeping README claims aligned with implemented behavior.
- Reviewing schema-template changes for synthetic sample data and clear tests.
- Keeping issue codes documented and stable.
- Avoiding unnecessary dependencies.
- Shipping releases only after CI, package build, and metadata checks pass.

## Decision Process

For now, decisions are made by the primary maintainer after public discussion in
issues or pull requests when practical. Changes should stay inside the project
scope: Japanese materials experiment CSV/XLSX table linting and normalization.

Large changes should be split into small pull requests. Scope expansions such as
OCR, LLM extraction, ELN/LIMS features, regulated compliance claims, or broad unit
conversion should first be discussed as roadmap issues.

## Release Process

Release steps are documented in [docs/release-checklist.md](docs/release-checklist.md).
Release notes should describe only behavior that is implemented and tested.

## New Maintainers

There are no additional maintainers yet. A future maintainer should have a history
of useful issues or pull requests, understand the privacy constraints around
experiment data, and follow the contribution and security policies.
