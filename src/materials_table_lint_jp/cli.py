from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .analyzer import analyze
from .reader import read_table
from .schema import load_schema, write_basic_schema
from .writer import render_json, render_summary, write_json, write_normalized_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mtlint",
        description="日本語材料実験CSV/Excelをschemaに沿って検査・正規化します。",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="basic schema JSONを生成します。")
    init_parser.add_argument("--out", type=Path, default=Path("schema.json"))

    inspect_parser = subparsers.add_parser("inspect", help="入力表のメタデータと列名を表示します。")
    inspect_parser.add_argument("input", type=Path)
    inspect_parser.add_argument("--sheet", help=".xlsx入力時のシート名")
    inspect_parser.add_argument("--json", action="store_true", dest="json_output")

    lint_parser = subparsers.add_parser("lint", help="schemaに沿って入力表を検査します。")
    add_common_table_args(lint_parser)
    lint_parser.add_argument("--report", type=Path, help="JSONレポートの出力先")
    lint_parser.add_argument("--json", action="store_true", dest="json_output")

    normalize_parser = subparsers.add_parser("normalize", help="検査して正規化CSVを書き出します。")
    add_common_table_args(normalize_parser)
    normalize_parser.add_argument("--out", type=Path, required=True, help="正規化CSVの出力先")
    normalize_parser.add_argument("--report", type=Path, help="JSONレポートの出力先")
    normalize_parser.add_argument("--json", action="store_true", dest="json_output")

    return parser


def add_common_table_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("input", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--sheet", help=".xlsx入力時のシート名")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            write_basic_schema(args.out)
            print(f"Wrote schema: {args.out}")
            return 0
        if args.command == "inspect":
            table = read_table(args.input, sheet=args.sheet)
            payload = {
                "input": str(table.path),
                "metadata": table.metadata,
                "headers": list(table.headers),
                "rows": len(table.rows),
            }
            if args.json_output:
                print(render_json(payload), end="")
            else:
                print(f"Input: {table.path}")
                print(f"Rows: {len(table.rows)}")
                print("Metadata:")
                for key, value in table.metadata.items():
                    print(f"  - {key}: {value}")
                print("Headers:")
                for header in table.headers:
                    print(f"  - {header}")
            return 0
        schema = load_schema(args.schema)
        table = read_table(args.input, sheet=args.sheet)
        analysis = analyze(table, schema)
        if args.command == "normalize":
            write_normalized_csv(args.out, analysis)
        report = analysis.to_report()
        if getattr(args, "report", None):
            write_json(args.report, report)
        if getattr(args, "json_output", False):
            print(render_json(report), end="")
        else:
            print(render_summary(analysis), end="")
        return 1 if analysis.status == "error" else 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"mtlint error: {exc}")
        return 2
