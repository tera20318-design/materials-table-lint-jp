# OpenAI Codex For Open Source Application Draft

## English Application Text

materials-table-lint-jp is a new OSS Python CLI for Japanese materials experiment tables. v0.1.1 checks simple CSV/XLSX files against explicit schemas for aliases, units, metadata, missing values, duplicate IDs, numeric parsing, and ranges. It includes basic, heat-treatment, and tensile-test templates, synthetic examples, tests, GitHub Actions CI, docs, and release notes. It has no stars, downloads, or adoption claims yet.

Character count: 426

## Japanese Intent Note

この申請文は、実績を盛らずに「日本語材料実験テーブルを再利用しやすくする小さなOSS」として説明するためのものです。既存のpymatgen、matminer、NOMAD、ELN系OSSと競うのではなく、その前段でExcel/CSVの表記ゆれを検査・正規化する薄い層として位置づけます。

## Field-Specific Drafts

### Repository Qualification

materials-table-lint-jp is a new OSS Python CLI for Japanese materials experiment tables. It checks simple CSV/XLSX files against explicit schemas for aliases, units, metadata, missing values, duplicate IDs, numeric parsing, and ranges. The repo includes synthetic examples, tests, GitHub Actions CI, governance, security notes, release notes, and a public roadmap. It has no adoption metrics yet.

### API Credit Use

The CLI does not require the OpenAI API at runtime. I would use API credits for OSS maintenance: Codex-assisted issue triage, pull request review, release-note drafting, documentation review, and turning reported CSV/XLSX edge cases into tests while avoiding uploads of private experiment data.

### Additional Note

This is a new public repository with no stars, downloads, or external adoption claims. The examples are synthetic. The project explicitly avoids OCR, LLM extraction, ELN/LIMS replacement, standards-compliance claims, and quality-assurance certification.

## Fact-Check Checklist

- [x] 新規repoで実績なしと書いているか。
- [x] PyPI未公開ならPyPI公開を主張していないか。
- [x] v0.1.1の実装範囲だけを書いているか。
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
