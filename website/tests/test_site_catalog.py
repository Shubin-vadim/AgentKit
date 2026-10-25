"""Tests for the website catalog generator."""

from pathlib import Path

import pytest

from agent_kit.library import Library
from site_catalog import (
    CatalogError,
    CatalogReader,
    PageRenderer,
    ReadmeTables,
    SkillEntry,
    SkillSource,
    SourceRule,
)
from site_catalog.utils import display_name, first_sentence, frontmatter, table_cell

SOURCE = SkillSource(label="up/stream", url="https://example.test/up", license="MIT")


def reader_for(kit: Path) -> CatalogReader:
    """Build a reader over a test kit.

    :param kit: The kit root.
    :return: A reader using the kit's README tables.
    """
    readme = (kit / "README.md").read_text(encoding="utf-8")
    return CatalogReader(Library([kit]), ReadmeTables(readme))


def test_first_sentence_keeps_only_the_first() -> None:
    assert first_sentence("Do X, e.g. this. Use when Y.") == "Do X, e.g. this."
    assert first_sentence("  One sentence  ") == "One sentence"


def test_display_name_uses_known_names_then_sentence_case() -> None:
    assert display_name("vllm") == "vLLM"
    assert display_name("reverse-engineering") == "Reverse engineering"


def test_table_cell_joins_lines_and_escapes_pipes() -> None:
    assert table_cell("a |\n b") == "a \\| b"


def test_frontmatter_reads_plain_and_folded_values() -> None:
    text = (
        "---\nname: 'x'\ndescription: >-\n  Line one\n  line two.\n"
        "metadata:\n  version: '1'\n---\nbody: no\n"
    )
    assert frontmatter(text) == {
        "name": "x",
        "description": "Line one line two.",
        "metadata": "",
    }
    assert frontmatter("# no frontmatter") == {}


def test_source_rule_covers_names_prefixes_and_exclusions() -> None:
    rule = SourceRule(
        names=("a",), prefixes=("kit-",), excluded=("kit-own",), source=SOURCE
    )
    assert rule.covers("a") and rule.covers("kit-one")
    assert not rule.covers("kit-own") and not rule.covers("b")


def test_readme_tables_read_sources_and_profiles(kit: Path) -> None:
    tables = ReadmeTables((kit / "README.md").read_text(encoding="utf-8"))
    (rule,) = tables.source_rules()
    assert rule.names == ("borrowed",)
    assert rule.prefixes == ("kit-",) and rule.excluded == ("kit-own",)
    assert rule.source == SOURCE
    assert tables.profile_summaries() == {
        "core": "Always added",
        "extra": "Extra things",
    }


def test_readme_tables_reject_missing_section_and_link() -> None:
    with pytest.raises(CatalogError, match="no '## Skill sources'"):
        ReadmeTables("# Kit\n").source_rules()
    broken = (
        "x\n## Skill sources\n\n| S | Src | L |\n|---|---|---|\n| `a` | none | MIT |\n"
    )
    with pytest.raises(CatalogError, match="no source link"):
        ReadmeTables(broken).source_rules()


def test_catalog_reader_lists_skills_with_groups_profiles_and_sources(
    kit: Path,
) -> None:
    skills = {s.name: s for s in reader_for(kit).skills()}
    assert skills["borrowed"].summary == "Borrowed skill."
    assert skills["borrowed"].profiles == ("core", "extra")
    assert skills["borrowed"].source == SOURCE
    assert skills["kit-one"].source == SOURCE
    assert skills["kit-own"].group == ("alpha", "deep")
    assert skills["kit-own"].source is None
    assert skills["solo"].profiles == ()


def test_catalog_reader_sorts_by_group_then_name(kit: Path) -> None:
    names = [s.name for s in reader_for(kit).skills()]
    assert names == ["borrowed", "kit-one", "kit-own", "solo"]


def test_catalog_reader_rejects_skill_without_description(kit: Path) -> None:
    (kit / "skills" / "beta" / "solo" / "SKILL.md").write_text("---\nname: solo\n---\n")
    with pytest.raises(CatalogError, match="no description"):
        reader_for(kit).skills()


def test_catalog_reader_lists_profiles_in_readme_order(kit: Path) -> None:
    profiles = reader_for(kit).profiles()
    assert [p.name for p in profiles] == ["core", "extra"]
    extra = profiles[1]
    assert extra.summary == "Extra things"
    assert extra.skills == ("kit-one", "borrowed")
    assert extra.rules == ("r1",) and extra.templates == ("docs/b.md",)


def test_page_renderer_skills_page(kit: Path) -> None:
    page = PageRenderer().skills_page(reader_for(kit).skills())
    assert "## Alpha" in page and "### Deep" in page and "## Beta" in page
    assert '<a id="borrowed"></a>`borrowed`' in page
    assert "[core](profiles.md#core)" in page
    assert "[up/stream](https://example.test/up)" in page
    assert "| Solo \\| piped skill. | — | Agent kit |" in page


def test_page_renderer_profiles_page(kit: Path) -> None:
    page = PageRenderer().profiles_page(reader_for(kit).profiles())
    assert "## extra" in page and "Extra things" in page
    assert "[`kit-one`](skills.md#kit-one)" in page
    assert "- **Rules:** `r1`" in page and "- **Templates:** `docs/b.md`" in page
    assert "MCP servers" not in page


def test_skill_entry_is_frozen() -> None:
    entry = SkillEntry(name="a", summary="s", group=("g",))
    with pytest.raises(ValueError, match="frozen"):
        entry.name = "b"  # type: ignore[misc]
