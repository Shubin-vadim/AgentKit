"""Tests for agent_kit.services: planner, installer, and lock."""

from pathlib import Path

import pytest
from recording_reporter import RecordingReporter

from agent_kit.clients import ClientRegistry
from agent_kit.errors import InstallError
from agent_kit.files import TargetWriter
from agent_kit.library import Library
from agent_kit.models import InstallRequest, KitLayout, LockContents
from agent_kit.services import (
    LOCK_NAME,
    Installer,
    InstallPlanner,
    LockWriter,
)


def request_for(target: Path, *clients: str) -> InstallRequest:
    """Build a request for the ``extra`` profile.

    :param target: The project folder.
    :param clients: Client names; none means detect.
    :return: The request.
    """
    return InstallRequest(target=target, clients=clients, profiles=("extra",))


def test_planner_resolves_everything(library: Library, target: Path) -> None:
    plan = InstallPlanner(library, ClientRegistry()).plan(request_for(target, "claude"))
    assert plan.selection.profiles == ("core", "extra")
    assert [r.name for r in plan.rules] == ["always", "scoped"]
    assert set(plan.servers) == {"local", "remote"}
    assert plan.client_source == "from --client"


def test_planner_detects_single_client(library: Library, target: Path) -> None:
    (target / ".cursor").mkdir()
    plan = InstallPlanner(library, ClientRegistry()).plan(request_for(target))
    assert plan.clients == ("cursor",)
    assert plan.client_source == "detected from .cursor"


def test_planner_refuses_ambiguous_target_and_the_kit(
    library: Library, target: Path, kit: KitLayout
) -> None:
    planner = InstallPlanner(library, ClientRegistry())
    with pytest.raises(InstallError, match="Ask the user"):
        planner.plan(request_for(target))
    with pytest.raises(InstallError, match="kit library"):
        planner.plan(request_for(kit.root, "cursor"))


def test_installer_writes_everything_and_reruns_cleanly(
    library: Library, kit: KitLayout, target: Path, reporter: RecordingReporter
) -> None:
    registry = ClientRegistry()
    plan = InstallPlanner(library, registry).plan(
        request_for(target, "claude", "codex")
    )
    installer = Installer(kit, registry, reporter)
    installer.install(plan, TargetWriter(target, reporter, force=False, dry_run=False))
    assert (target / ".claude/skills/helper/references/notes.md").is_file()
    assert (target / ".agents/skills/helper/SKILL.md").is_file()
    assert (target / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n"
    assert (target / LOCK_NAME).is_file()
    assert (
        "note: Codex reads .codex/config.toml only in trusted projects."
        in reporter.infos
    )
    rerun = RecordingReporter()
    Installer(kit, registry, rerun).install(
        plan, TargetWriter(target, rerun, force=False, dry_run=False)
    )
    assert "skip" in rerun.verbs()


def test_installer_dry_run_writes_nothing(
    library: Library, kit: KitLayout, target: Path, reporter: RecordingReporter
) -> None:
    registry = ClientRegistry()
    plan = InstallPlanner(library, registry).plan(request_for(target, "cursor"))
    Installer(kit, registry, reporter).install(
        plan, TargetWriter(target, reporter, force=False, dry_run=True)
    )
    assert list(target.iterdir()) == []


def test_lock_writer_records_lists(kit: KitLayout, writer: TargetWriter) -> None:
    contents = LockContents(
        kit_root=kit.root,
        libraries=(),
        clients=("claude",),
        profiles=("core",),
        skills=("helper",),
        rules=(),
        mcp=("local",),
        templates=("AGENTS.md",),
    )
    LockWriter().write(writer, contents)
    lock = (writer.root / LOCK_NAME).read_text(encoding="utf-8")
    assert "clients:\n  - claude" in lock
    assert "rules: []" in lock
    assert "libraries" not in lock
