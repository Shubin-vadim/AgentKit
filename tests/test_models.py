"""Tests for the methods on agent_kit.models."""

from pathlib import Path

from agent_kit.models import AssetKind, KitLayout, Rule, TemplateSpec


def test_kit_layout_defaults() -> None:
    assert KitLayout(root=Path("kit")).library_dirs == ()


def test_asset_kind_names_by_folder_or_stem() -> None:
    skill = AssetKind(
        label="skill", folder="skills", pattern="SKILL.md", named_by_folder=True
    )
    rule = AssetKind(label="rule", folder="rules", pattern="*.mdc")
    assert skill.name_of(Path("skills/x/helper/SKILL.md")) == "helper"
    assert rule.name_of(Path("rules/core/always.mdc")) == "always"


def test_template_spec_parse_with_and_without_arrow() -> None:
    assert TemplateSpec.parse("a/b.md => c.md") == TemplateSpec(
        src="a/b.md", dest="c.md"
    )
    assert TemplateSpec.parse("AGENTS.md") == TemplateSpec(
        src="AGENTS.md", dest="AGENTS.md"
    )


def test_rule_scope_ignores_globs_when_always() -> None:
    assert Rule(name="r", source="", body="", globs=("*.py",), always=True).scope == ()
    assert Rule(name="r", source="", body="", globs=("*.py",)).scope == ("*.py",)


def test_rule_scope_note() -> None:
    scoped = Rule(name="r", source="", body="", globs=("*.py", "a.md"))
    assert (
        scoped.scope_note()
        == "_Applies when working on files matching: `*.py`, `a.md`._\n\n"
    )
    assert Rule(name="r", source="", body="").scope_note() == ""


def test_rule_demoted_body_skips_code_fences() -> None:
    rule = Rule(name="r", source="", body="# Title\n```\n# not a heading\n```\n## Sub")
    assert rule.demoted_body() == "## Title\n```\n# not a heading\n```\n### Sub"
