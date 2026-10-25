"""Tests for agent_kit.cli.KitCli."""

from pathlib import Path

from recording_reporter import RecordingReporter
from utils import write

from agent_kit.cli import KitCli
from agent_kit.models import KitLayout


def test_build_parser_knows_every_command(kit: KitLayout) -> None:
    parser = KitCli(kit, RecordingReporter()).build_parser()
    args = parser.parse_args(["install", "--target", "x", "--client", "claude"])
    assert (args.command, args.client) == ("install", "claude")


def test_run_list_and_check(kit: KitLayout, reporter: RecordingReporter) -> None:
    cli = KitCli(kit, reporter)
    assert cli.run(["list"]) == 0
    assert cli.run(["check"]) == 0
    assert reporter.infos == ["core", "extra", "Library OK."]


def test_run_check_fails_on_problems(
    kit: KitLayout, reporter: RecordingReporter
) -> None:
    write(kit.root / "profiles" / "bad.yaml", "name: bad\nskills:\n  - ghost\n")
    assert KitCli(kit, reporter).run(["check"]) == 1
    assert reporter.errors


def test_run_detect(kit: KitLayout, target: Path, reporter: RecordingReporter) -> None:
    (target / ".codex").mkdir()
    assert KitCli(kit, reporter).run(["detect", "--target", str(target)]) == 0
    assert reporter.infos[-1] == "detected: codex"


def test_run_install_dry_run(
    kit: KitLayout, target: Path, reporter: RecordingReporter
) -> None:
    code = KitCli(kit, reporter).run(
        ["install", "--target", str(target), "--client", "cursor", "--dry-run"]
    )
    assert code == 0
    assert reporter.infos[-1] == "\nDry run. No files written."
    assert list(target.iterdir()) == []


def test_run_reports_app_errors(
    kit: KitLayout, target: Path, reporter: RecordingReporter
) -> None:
    code = KitCli(kit, reporter).run(
        ["install", "--target", str(target), "--client", "vim"]
    )
    assert code == 1
    assert "Unknown client 'vim'" in reporter.errors[0]
