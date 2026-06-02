# Security Policy

## Supported Versions

This is a new project. Security fixes are handled on the latest released version.

## Reporting A Vulnerability

Please open a GitHub issue with a minimal reproduction unless the report includes
sensitive information. Do not paste real experiment data, customer names, lot
numbers, internal material codes, or confidential measurements.

Use GitHub private vulnerability reporting if it is enabled. If not, open a minimal
public issue that does not include sensitive details and ask for a private contact path.

## Security Notes

- The CLI reads local CSV/XLSX files and writes local outputs.
- It does not send telemetry.
- It does not upload data to external services.
- It does not perform network calls by default.
- Redaction is not part of current releases. Review reports and normalized files before sharing.
- JSON reports can include raw metadata values, column names, issue values, and input paths.
- The tool is a data-quality aid, not a regulated quality assurance decision system.
