# OpenAI Codex For Open Source Application Draft

## English Application Text

materials-table-lint-jp is a new OSS Python CLI for Japanese materials experiment tables. v0.1.0 checks simple tabular CSV/XLSX files against explicit schemas for aliases, units, metadata, missing values, duplicate sample IDs, duplicate mapped columns, numeric parsing, and simple ranges. It writes JSON reports and normalized CSV when checks pass. The repo includes examples, tests, GitHub Actions CI, docs, and release notes. It has no adoption metrics yet.

Character count: 459

## Japanese Intent Note

この申請文は、実績を盛らずに「日本語材料実験テーブルを再利用しやすくする小さなOSS」として説明するためのものです。既存のpymatgen、matminer、NOMAD、ELN系OSSと競うのではなく、その前段でExcel/CSVの表記ゆれを検査・正規化する薄い層として位置づけます。

## Fact-Check Checklist

- [x] 新規repoで実績なしと書いているか。
- [x] PyPI未公開ならPyPI公開を主張していないか。
- [x] v0.1.0の実装範囲だけを書いているか。
- [x] OCR、AI抽出、ELN/LIMS、品質保証判定を主張していないか。
- [x] tests、CI、README、examples、release notes がrepo内で確認できるか。

## Do Not Write

- "widely used"
- "trusted by materials engineers"
- "complete ELN"
- "LIMS replacement"
- "JIS compliant"
- "quality assurance certified"
- "extracts any PDF"
- "AI-powered automatic interpretation"
- "guarantees clean data"
