# materials-table-lint-jp

日本語の材料実験CSV/Excelを、解析や共有に使いやすい形へ整えるための小さなCLIです。

`mtlint` は、材料実験表の列名ゆれ、単位表記、必須メタデータ、欠損値、サンプルID重複、数値範囲をスキーマに沿って検査し、正規化CSVとJSONレポートを出力します。

このプロジェクトは新しいOSSです。stars、downloads、外部採用事例などの実績はまだありません。

## What It Does

- CSVを標準ライブラリだけで読み込みます。
- `.xlsx` は optional dependency の `openpyxl` を入れた場合だけ読み込みます。
- `# key=value` 形式の先頭メタデータを読み取ります。
- 日本語・英語・略称の列名を schema alias で標準名に寄せます。
- `温度[℃]` や `引張強さ[MPa]` のような列名内単位を検査します。
- 必須列、必須メタデータ、空欄、重複サンプルID、数値変換、範囲外値を報告します。
- 正規化CSVとJSONレポートを出力します。

## Not In Scope

- 任意レイアウトの複雑なExcel帳票解析
- PDF/OCR/LLMによる自動抽出
- ELN/LIMS/材料DBの代替
- JISなど規格本文の同梱や適合判定
- 品質保証上の合否判定
- 単位換算の網羅実装

## Installation

まだPyPIには公開していません。GitHubから取得してローカルインストールできます。

```bash
git clone https://github.com/tera20318-design/materials-table-lint-jp.git
cd materials-table-lint-jp
python -m pip install .
```

Excel `.xlsx` も読む場合:

```bash
python -m pip install ".[xlsx]"
```

開発用:

```bash
python -m pip install -e ".[dev,xlsx]"
```

## Quick Start

スキーマを生成:

```bash
mtlint init --out schema.json
```

正常なサンプルCSVを検査:

```bash
mtlint lint examples/clean.csv --schema examples/basic.schema.json
```

正規化CSVとJSONレポートを出力:

```bash
mtlint normalize examples/clean.csv --schema examples/basic.schema.json --out normalized.csv --report report.json
```

列とメタデータだけ確認:

```bash
mtlint inspect examples/sample.csv
```

issueを含むサンプルを確認:

```bash
mtlint lint examples/sample.csv --schema examples/basic.schema.json
```

## Example Input

```csv
# project=Al合金熱処理
# operator=Tanaka
# date=2026-06-01
試料ID,温度[℃],保持時間[min],引張強さ[MPa],破断伸び[%],備考
A-001,520,60,310,12.5,
A-002,520,,305,,
A-002,540,30,,10.1,再測定予定
```

## Example Issues

`mtlint lint` は、たとえば次のような issue code を出します。

- `MISSING_METADATA`
- `MISSING_REQUIRED_COLUMN`
- `UNIT_MISMATCH`
- `MISSING_VALUE`
- `DUPLICATE_SAMPLE_ID`
- `NUMERIC_PARSE_ERROR`
- `RANGE_VIOLATION`
- `UNKNOWN_COLUMN`

## Exit Codes

- `0`: errors がなく、warnings のみまたは問題なし。
- `1`: `error` severity のissueがある。
- `2`: 入力ファイル、schema、引数、依存関係などCLI実行自体のエラー。

## Privacy And Security

- このCLIはローカルファイルだけを読み書きします。
- テレメトリ、外部アップロード、ネットワーク通信はありません。
- サンプルデータは合成データです。
- 実験データには材料名、ロット、顧客名、装置名、社内コードなどが含まれることがあります。JSONレポートや正規化CSVを共有する前に内容を確認してください。

## Development

```bash
python -m pip install -e ".[dev,xlsx]"
ruff format --check .
ruff check .
mypy src tests
pytest
python -m build
python -m twine check dist/*
```

## Roadmap

今後の候補は [docs/roadmap.md](docs/roadmap.md) に分離しています。READMEには現在動く機能だけを書きます。

## License

MIT License. See [LICENSE](LICENSE).
