"""Tests for agent_kit.library: Library, parsers, validator."""

from pathlib import Path

import pytest
from utils import LOCAL_SERVER, build_kit, write

from agent_kit.errors import LibraryError
from agent_kit.library import (
    SKILL,
    Library,
    LibraryValidator,
    McpFragmentLoader,
    ProfileParser,
    RuleParser,
)
from agent_kit.models import KitLayout, RemoteServer, StdioServer


def test_discover_adds_layout_folders(kit: KitLayout, tmp_path: Path) -> None:
    extra = tmp_path / "extra"
    extra.mkdir()
    layout = kit.model_copy(update={"library_dirs": (extra, extra)})
    assert Library.discover(layout).extra_roots == [extra.resolve()]
    assert Library.discover(kit).extra_roots == []


def test_discover_rejects_missing_folder(kit: KitLayout, tmp_path: Path) -> None:
    layout = kit.model_copy(update={"library_dirs": (tmp_path / "none",)})
    with pytest.raises(LibraryError, match="none"):
        Library.discover(layout)


def test_extra_roots_excludes_the_kit(library: Library) -> None:
    assert library.extra_roots == []


def test_contains_kit_and_children(
    library: Library, kit: KitLayout, target: Path
) -> None:
    assert library.contains(kit.root)
    assert library.contains(kit.root / "skills")
    assert not library.contains(target)


def test_index_maps_names_to_files(library: Library) -> None:
    assert list(library.index(SKILL)) == ["helper"]


def test_asset_lookups(library: Library, kit: KitLayout) -> None:
    assert library.skill("helper") == kit.root / "skills" / "group" / "helper"
    assert library.rule("always").name == "always.mdc"
    assert library.mcp_fragment("local").name == "local.json"
    with pytest.raises(LibraryError):
        library.skill("missing")


def test_duplicate_asset_is_an_error(kit: KitLayout, tmp_path: Path) -> None:
    other = build_kit(tmp_path / "other")
    library = Library.discover(kit.model_copy(update={"library_dirs": (other,)}))
    with pytest.raises(LibraryError, match="Duplicate"):
        library.rule("always")


def test_template_candidates_and_template(library: Library, kit: KitLayout) -> None:
    assert library.template_candidates("AGENTS.md") == [
        kit.root / "templates" / "AGENTS.md"
    ]
    assert library.template("AGENTS.md").name == "AGENTS.md"
    with pytest.raises(LibraryError, match="missing"):
        library.template("none.md")


def test_profile_names_and_profile(library: Library) -> None:
    assert library.profile_names() == ["core", "extra"]
    assert library.profile("extra").rules == ("scoped",)
    with pytest.raises(LibraryError, match="Unknown profile"):
        library.profile("nope")


def test_select_adds_core_and_deduplicates(library: Library) -> None:
    selection = library.select(["extra", "extra"], include_core=True)
    assert selection.profiles == ("core", "extra")
    assert selection.rules == ("always", "scoped")
    assert library.select(["extra"], include_core=False).profiles == ("extra",)


def test_profile_parser_reads_lists(kit: KitLayout) -> None:
    profile = ProfileParser().parse(kit.root / "profiles" / "core.yaml")
    assert (profile.name, profile.skills, profile.mcp) == (
        "core",
        ("helper",),
        ("local",),
    )
    assert profile.templates[0].dest == "AGENTS.md"


def test_rule_parser_reads_scope_and_body(kit: KitLayout) -> None:
    scoped = RuleParser().parse(kit.root / "rules" / "py" / "scoped.mdc")
    assert scoped.globs == ("**/*.py", "docs/a.md")
    assert not scoped.always
    assert scoped.body.startswith("# Py")
    assert RuleParser().parse(kit.root / "rules" / "core" / "always.mdc").always


def test_mcp_loader_builds_models_and_rejects_invalid(
    kit: KitLayout, tmp_path: Path
) -> None:
    local = McpFragmentLoader().load(kit.root / "mcp" / "local" / "local.json")
    assert local["local"] == StdioServer(**LOCAL_SERVER["local"])
    remote = McpFragmentLoader().load(kit.root / "mcp" / "remote" / "remote.json")
    assert isinstance(remote["remote"], RemoteServer)
    with pytest.raises(LibraryError):
        McpFragmentLoader().load(write(tmp_path / "bad.json", '{"x": {"nope": 1}}'))


def test_validator_accepts_clean_library(library: Library) -> None:
    assert LibraryValidator().problems(library) == []


def test_validator_reports_dangling_entries(kit: KitLayout) -> None:
    write(
        kit.root / "profiles" / "broken.yaml",
        "name: broken\nskills:\n  - ghost\ntemplates:\n  - none.md\n",
    )
    problems = LibraryValidator().problems(Library.discover(kit))
    assert any("unknown skill 'ghost'" in p for p in problems)
    assert any("none.md" in p for p in problems)
