"""Tests for agent_kit.files: ManagedBlock, TargetWriter, FolderSync."""

import json
from pathlib import Path

import pytest
from recording_reporter import RecordingReporter
from utils import write

from agent_kit.errors import ConfigFileError
from agent_kit.files import FolderSync, ManagedBlock, TargetWriter

BLOCK = ManagedBlock(begin="<!-- b -->", end="<!-- e -->")


def test_managed_block_inner_and_outside() -> None:
    text = "mine\n<!-- b -->\nkit\n<!-- e -->\nafter"
    assert BLOCK.inner(text) == "kit\n"
    assert BLOCK.outside(text) == "mine\n\nafter"
    assert BLOCK.inner("no block") == ""


def test_managed_block_put_appends_then_replaces() -> None:
    first = BLOCK.put("mine", "v1")
    assert first == "mine\n\n<!-- b -->\nv1\n<!-- e -->\n"
    assert BLOCK.put(first, "v2") == "mine\n\n<!-- b -->\nv2\n<!-- e -->\n"
    assert BLOCK.put("", "v1") == "<!-- b -->\nv1\n<!-- e -->\n"


def test_report_uses_relative_paths(
    writer: TargetWriter, reporter: RecordingReporter
) -> None:
    writer.report("write", writer.root / "a" / "b.md", "note")
    assert reporter.actions == [("write", "a/b.md", "note")]


def test_warn_collects_messages(writer: TargetWriter) -> None:
    writer.warn("fix me")
    assert writer.warnings == ["fix me"]


def test_write_text_respects_dry_run(target: Path, reporter: RecordingReporter) -> None:
    dry = TargetWriter(target, reporter, force=False, dry_run=True)
    dry.write_text(target / "x.md", "x")
    assert not (target / "x.md").exists()


def test_write_unless_present_skips_then_forces(
    target: Path, reporter: RecordingReporter
) -> None:
    path = write(target / "a.md", "old")
    TargetWriter(target, reporter, force=False, dry_run=False).write_unless_present(
        path, "new"
    )
    assert path.read_text(encoding="utf-8") == "old"
    TargetWriter(target, reporter, force=True, dry_run=False).write_unless_present(
        path, "new"
    )
    assert path.read_text(encoding="utf-8") == "new"
    assert reporter.verbs() == ["skip", "replace"]


def test_read_json_missing_invalid_and_non_object(writer: TargetWriter) -> None:
    assert writer.read_json(writer.root / "none.json") == {}
    with pytest.raises(ConfigFileError):
        writer.read_json(write(writer.root / "bad.json", "{"))
    with pytest.raises(ConfigFileError):
        writer.read_json(write(writer.root / "list.json", "[]"))


def test_write_json_formats_with_indent(writer: TargetWriter) -> None:
    writer.write_json(writer.root / "c.json", {"a": 1})
    assert (writer.root / "c.json").read_text(encoding="utf-8") == '{\n  "a": 1\n}\n'


def test_set_defaults_keeps_existing_values(writer: TargetWriter) -> None:
    path = write(writer.root / "c.json", json.dumps({"a": 1}))
    writer.set_defaults(path, {"a": 2, "$schema": "s"})
    assert writer.read_json(path) == {"$schema": "s", "a": 1}


def test_merge_entries_skips_existing_unless_forced(
    target: Path, reporter: RecordingReporter
) -> None:
    path = write(target / "m.json", json.dumps({"mcpServers": {"x": {"v": 1}}}))
    TargetWriter(target, reporter, force=False, dry_run=False).merge_entries(
        path, "mcpServers", {"x": {"v": 2}, "y": {"v": 3}}
    )
    assert json.loads(path.read_text(encoding="utf-8"))["mcpServers"] == {
        "x": {"v": 1},
        "y": {"v": 3},
    }
    TargetWriter(target, reporter, force=True, dry_run=False).merge_entries(
        path, "mcpServers", {"x": {"v": 2}}
    )
    assert json.loads(path.read_text(encoding="utf-8"))["mcpServers"]["x"] == {"v": 2}


def test_merge_entries_rejects_non_object_section(writer: TargetWriter) -> None:
    path = write(writer.root / "m.json", json.dumps({"mcp": []}))
    with pytest.raises(ConfigFileError):
        writer.merge_entries(path, "mcp", {"x": {}})


def test_files_of_skips_python_caches(tmp_path: Path) -> None:
    write(tmp_path / "SKILL.md", "s")
    write(tmp_path / "__pycache__" / "m.pyc", "c")
    write(tmp_path / "tool.pyc", "c")
    assert FolderSync().files_of(tmp_path) == {Path("SKILL.md")}


def test_sync_copies_and_removes_stale(tmp_path: Path) -> None:
    src, dest = tmp_path / "src", tmp_path / "dest"
    write(src / "SKILL.md", "new")
    write(src / "refs" / "a.md", "a")
    write(dest / "SKILL.md", "old")
    write(dest / "stale" / "gone.md", "x")
    FolderSync().sync(src, dest)
    assert (dest / "SKILL.md").read_text(encoding="utf-8") == "new"
    assert (dest / "refs" / "a.md").is_file()
    assert not (dest / "stale").exists()
