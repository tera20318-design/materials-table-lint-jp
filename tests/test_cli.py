from pathlib import Path
from typing import Any

from materials_table_lint_jp import cli
from materials_table_lint_jp.cli import main

REPO_ROOT = Path(__file__).resolve().parents[1]


class FakeTextStream:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def reconfigure(self, **kwargs: Any) -> None:
        self.calls.append(kwargs)


def test_configure_cli_output_uses_utf8(monkeypatch) -> None:
    stdout = FakeTextStream()
    stderr = FakeTextStream()

    monkeypatch.setattr(cli.sys, "stdout", stdout)
    monkeypatch.setattr(cli.sys, "stderr", stderr)

    cli.configure_cli_output()

    assert stdout.calls == [{"encoding": "utf-8", "errors": "replace"}]
    assert stderr.calls == [{"encoding": "utf-8", "errors": "replace"}]


def test_cli_init_and_lint_clean_sample(tmp_path: Path, capsys) -> None:
    schema = tmp_path / "schema.json"
    assert main(["init", "--out", str(schema)]) == 0

    data = tmp_path / "clean.csv"
    data.write_text(
        "\n".join(
            [
                "# project=Synthetic example",
                "# operator=Example Operator",
                "# date=2026-06-01",
                "試料ID,温度[℃],保持時間[min],引張強さ[MPa],破断伸び[%],備考",
                "SYN-001,520,60,310,12.5,",
            ]
        ),
        encoding="utf-8",
    )

    assert main(["lint", str(data), "--schema", str(schema)]) == 0
    output = capsys.readouterr().out
    assert "Status: ok" in output


def test_cli_init_template_and_lint_tensile_sample(tmp_path: Path) -> None:
    schema = tmp_path / "tensile.schema.json"
    assert main(["init", "--template", "tensile-test", "--out", str(schema)]) == 0

    data = tmp_path / "tensile.csv"
    data.write_text(
        "\n".join(
            [
                "# project=Synthetic tensile screening",
                "# operator=Example Operator",
                "# date=2026-06-02",
                "# test_method=room temperature tensile test",
                "試料ID,試験片No,材質,標点間距離[mm],耐力[MPa],引張強さ[MPa],破断伸び[%],破断位置,備考",
                "SYN-T-001,1,SYN-MAT,50,245,310,12.5,中央,",
            ]
        ),
        encoding="utf-8",
    )

    assert main(["lint", str(data), "--schema", str(schema)]) == 0


def test_material_examples_lint_cleanly() -> None:
    examples = REPO_ROOT / "examples"

    assert (
        main(
            [
                "lint",
                str(examples / "heat_treatment.csv"),
                "--schema",
                str(examples / "heat_treatment.schema.json"),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "lint",
                str(examples / "tensile_test.csv"),
                "--schema",
                str(examples / "tensile_test.schema.json"),
            ]
        )
        == 0
    )


def test_cli_normalize_writes_outputs(tmp_path: Path) -> None:
    schema = tmp_path / "schema.json"
    main(["init", "--out", str(schema)])
    data = tmp_path / "data.csv"
    data.write_text(
        "\n".join(
            [
                "# project=Synthetic example",
                "# operator=Example Operator",
                "# date=2026-06-01",
                "試料ID,温度[℃],保持時間[min]",
                "SYN-001,520,60",
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


def test_cli_normalize_does_not_write_csv_on_error(tmp_path: Path) -> None:
    schema = tmp_path / "schema.json"
    main(["init", "--out", str(schema)])
    data = tmp_path / "bad.csv"
    data.write_text("試料ID,温度[℃]\nA-001,500\n", encoding="utf-8")
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

    assert code == 1
    assert not out.exists()
    assert '"status": "error"' in report.read_text(encoding="utf-8")


def test_cli_inspect_json(tmp_path: Path, capsys) -> None:
    data = tmp_path / "data.csv"
    data.write_text("# project=Demo\n試料ID,温度[℃]\nA-001,500\n", encoding="utf-8")

    assert main(["inspect", str(data), "--json"]) == 0

    output = capsys.readouterr().out
    assert '"headers"' in output
    assert "試料ID" in output
