from pathlib import Path

from materials_table_lint_jp.cli import main


def test_cli_init_and_lint_clean_sample(tmp_path: Path, capsys) -> None:
    schema = tmp_path / "schema.json"
    assert main(["init", "--out", str(schema)]) == 0

    data = tmp_path / "clean.csv"
    data.write_text(
        "\n".join(
            [
                "# project=Al",
                "# operator=Tanaka",
                "# date=2026-06-01",
                "試料ID,温度[℃],保持時間[min],引張強さ[MPa],破断伸び[%],備考",
                "A-001,520,60,310,12.5,",
            ]
        ),
        encoding="utf-8",
    )

    assert main(["lint", str(data), "--schema", str(schema)]) == 0
    output = capsys.readouterr().out
    assert "Status: ok" in output


def test_cli_normalize_writes_outputs(tmp_path: Path) -> None:
    schema = tmp_path / "schema.json"
    main(["init", "--out", str(schema)])
    data = tmp_path / "data.csv"
    data.write_text(
        "\n".join(
            [
                "# project=Al",
                "# operator=Tanaka",
                "# date=2026-06-01",
                "試料ID,温度[℃],保持時間[min]",
                "A-001,520,60",
            ]
        ),
        encoding="utf-8",
    )
    out = tmp_path / "normalized.csv"
    report = tmp_path / "report.json"

    code = main(
        [
            "normalize",
            str(data),
            "--schema",
            str(schema),
            "--out",
            str(out),
            "--report",
            str(report),
        ]
    )

    assert code == 0
    assert out.read_text(encoding="utf-8").splitlines()[0].startswith("sample_id,temperature_degC")
    assert '"status": "ok"' in report.read_text(encoding="utf-8")


def test_cli_lint_returns_nonzero_for_error(tmp_path: Path) -> None:
    schema = tmp_path / "schema.json"
    main(["init", "--out", str(schema)])
    data = tmp_path / "bad.csv"
    data.write_text("試料ID,温度[℃]\nA-001,500\n", encoding="utf-8")

    assert main(["lint", str(data), "--schema", str(schema), "--json"]) == 1


def test_cli_inspect_json(tmp_path: Path, capsys) -> None:
    data = tmp_path / "data.csv"
    data.write_text("# project=Demo\n試料ID,温度[℃]\nA-001,500\n", encoding="utf-8")

    assert main(["inspect", str(data), "--json"]) == 0

    output = capsys.readouterr().out
    assert '"headers"' in output
    assert "試料ID" in output
