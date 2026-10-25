"""Collect the public skills and profiles of the kit for the website."""

import logging
from pathlib import Path

from agent_kit.library import SKILL, Library
from site_catalog.errors import CatalogError
from site_catalog.models import ProfileEntry, SkillEntry, SkillSource, SourceRule
from site_catalog.readme_tables import ReadmeTables
from site_catalog.utils import first_sentence, frontmatter

logger = logging.getLogger(__name__)

DESCRIPTION_KEY = "description"


class CatalogReader:
    """Reads skills, profiles, and skill sources from one public library."""

    def __init__(self, library: Library, tables: ReadmeTables) -> None:
        self._library = library
        self._tables = tables

    def skills(self) -> list[SkillEntry]:
        """List every skill with its summary, folder group, profiles, and source.

        :return: Skills sorted by group, then name.
        :raises CatalogError: If a skill has no description or appears twice.
        """
        rules = self._tables.source_rules()
        profiles_of = self._profiles_by_skill()
        entries = [
            self._entry(name, paths, profiles_of.get(name, ()), rules)
            for name, paths in self._library.index(SKILL).items()
        ]
        logger.debug("catalog has %d skills", len(entries))
        return sorted(entries, key=lambda e: (e.group, e.name))

    def profiles(self) -> list[ProfileEntry]:
        """List every profile with its README summary and contents.

        :return: Profiles in README order, then any profile the README omits.
        :raises CatalogError: If the README has no profiles table.
        """
        summaries = self._tables.profile_summaries()
        names = self._library.profile_names()
        ordered = [n for n in summaries if n in names]
        ordered += [n for n in names if n not in summaries]
        return [self._profile_entry(name, summaries.get(name, "")) for name in ordered]

    def _profile_entry(self, name: str, summary: str) -> ProfileEntry:
        profile = self._library.profile(name)
        return ProfileEntry(
            name=name,
            summary=summary,
            skills=profile.skills,
            rules=profile.rules,
            mcp=profile.mcp,
            templates=tuple(t.dest for t in profile.templates),
        )

    def _profiles_by_skill(self) -> dict[str, tuple[str, ...]]:
        found: dict[str, list[str]] = {}
        for name in self._library.profile_names():
            for skill in self._library.profile(name).skills:
                found.setdefault(skill, []).append(name)
        return {skill: tuple(names) for skill, names in found.items()}

    def _entry(
        self,
        name: str,
        paths: list[Path],
        profiles: tuple[str, ...],
        rules: list[SourceRule],
    ) -> SkillEntry:
        if len(paths) != 1:
            raise CatalogError(f"Skill '{name}' is defined {len(paths)} times: {paths}")
        skill_file = paths[0]
        description = frontmatter(skill_file.read_text(encoding="utf-8")).get(
            DESCRIPTION_KEY, ""
        )
        if not description:
            raise CatalogError(f"Skill '{name}' has no description: {skill_file}")
        return SkillEntry(
            name=name,
            summary=first_sentence(description),
            group=self._group(skill_file),
            profiles=profiles,
            source=self._source(name, rules),
        )

    def _group(self, skill_file: Path) -> tuple[str, ...]:
        for root in self._library.roots:
            base = root / SKILL.folder
            if base in skill_file.parents:
                return skill_file.parent.parent.relative_to(base).parts
        raise CatalogError(f"Skill file is outside every library: {skill_file}")

    @staticmethod
    def _source(name: str, rules: list[SourceRule]) -> SkillSource | None:
        return next((rule.source for rule in rules if rule.covers(name)), None)
