"""Read the tables in the README that the website reuses."""

import re

from site_catalog.errors import CatalogError
from site_catalog.models import SkillSource, SourceRule

TABLE_ROW = "|"
SEPARATOR_ROW = re.compile(r"^\|[\s:|-]+\|$")
CODE_SPAN = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
EXCEPT_WORD = "except"
WILDCARD = "*"
SOURCES_HEADING = "## Skill sources"
PROFILES_HEADING = "## Profiles"
SOURCE_COLUMNS = 3


class ReadmeTables:
    """Extracts the skill sources and profile summaries from README tables."""

    def __init__(self, readme: str) -> None:
        self._readme = readme

    def source_rules(self) -> list[SourceRule]:
        """Read the "Skill sources" table.

        :return: One rule per row, in README order.
        :raises CatalogError: If the section or its table is missing or malformed.
        """
        return [self._source_rule(row) for row in self._rows(SOURCES_HEADING)]

    def profile_summaries(self) -> dict[str, str]:
        """Read the "Profiles" table.

        :return: Profile name to its one-line description.
        :raises CatalogError: If the section or its table is missing.
        """
        summaries: dict[str, str] = {}
        for cells in self._rows(PROFILES_HEADING):
            names = CODE_SPAN.findall(cells[0])
            if names:
                summaries[names[0]] = cells[1]
        return summaries

    def _rows(self, heading: str) -> list[list[str]]:
        lines = self._section(heading).splitlines()
        table = [line.strip() for line in lines if line.strip().startswith(TABLE_ROW)]
        rows = [line for line in table[1:] if not SEPARATOR_ROW.match(line)]
        if not rows:
            raise CatalogError(f"README section '{heading}' has no table rows.")
        return [[cell.strip() for cell in row.strip("|").split("|")] for row in rows]

    def _section(self, heading: str) -> str:
        start = self._readme.find(f"\n{heading}\n")
        if start < 0:
            raise CatalogError(f"README has no '{heading}' section.")
        body = self._readme[start + len(heading) + 2 :]
        end = body.find("\n## ")
        return body if end < 0 else body[:end]

    @staticmethod
    def _source_rule(cells: list[str]) -> SourceRule:
        link = LINK.search(cells[1]) if len(cells) >= SOURCE_COLUMNS else None
        if link is None:
            raise CatalogError(f"Skill sources row has no source link: {cells}")
        included, _, excluded = cells[0].partition(EXCEPT_WORD)
        names = CODE_SPAN.findall(included)
        return SourceRule(
            names=tuple(n for n in names if not n.endswith(WILDCARD)),
            prefixes=tuple(n[:-1] for n in names if n.endswith(WILDCARD)),
            excluded=tuple(CODE_SPAN.findall(excluded)),
            source=SkillSource(label=link[1], url=link[2], license=cells[2]),
        )
