# Schema Template Request

## Experiment Type

Example: heat treatment, tensile test, XRD, coating test.

## Table Shape

Describe the expected columns without posting confidential data.

```csv
# project=synthetic example
# operator=Example
# date=2026-06-02
試料ID,列名1[unit],列名2[unit]
SYN-001,1.0,2.0
```

## Required Checks

- [ ] Required metadata
- [ ] Required columns
- [ ] Unit notation
- [ ] Numeric parsing
- [ ] Simple range checks
- [ ] Duplicate sample IDs

## Safety Checklist

- [ ] The example is synthetic or cleared for public sharing.
- [ ] I removed customer names, real lot numbers, internal material codes, and confidential measurements.
- [ ] I am not requesting a regulated pass/fail or standards-compliance decision.
