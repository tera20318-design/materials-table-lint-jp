# OpenAI Codex For Open Source Application Draft

## English Application Text

materials-table-lint-jp is a new OSS Python CLI for Japanese materials experiment tables. v0.1.0 checks CSV/XLSX data against explicit schemas for column aliases, units, required metadata, missing values, sample ID duplication, numeric parsing, and simple ranges; then writes JSON reports and normalized CSV. It is scoped as a local pre-analysis data-quality tool, not an ELN, LIMS, OCR, or AI extraction system. It is new and has no adoption metrics yet.

Character count: 455

## Japanese Intent Note

この申請文は、実績を盛らずに「日本語材料実験テーブルを再利用しやすくする小さなOSS」として説明するためのものです。既存のpymatgen、matminer、NOMAD、ELN系OSSと競うのではなく、その前段でExcel/CSVの表記ゆれを検査・正規化する薄い層として位置づけます。

## Fact-Check Checklist

- [ ] 新規repoで実績なしと書いているか。
- [ ] PyPI未公開ならPyPI公開を主張していないか。
- [ ] v0.1.0の実装範囲だけを書いているか。
- [ ] OCR、AI抽出、ELN/LIMS、品質保証判定を主張していないか。
- [ ] tests、CI、README、examples、release notes がrepo内で確認できるか。

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
