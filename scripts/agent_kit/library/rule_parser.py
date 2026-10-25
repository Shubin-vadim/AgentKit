"""Read ``.mdc`` rule sources."""

import re
from pathlib import Path

from agent_kit.models import Rule

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?", re.S)
QUOTES = "\"'"


class RuleParser:
    """Parses a rule's frontmatter (``globs``, ``alwaysApply``) and body."""

    def parse(self, path: Path) -> Rule:
        """Read one rule file.

        :param path: A ``rules/**/<name>.mdc`` file.
        :return: The rule, named after the file.
        """
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        fields = self._fields(match.group(1)) if match else {}
        body = text[match.end() :].lstrip("\n") if match else text
        globs = tuple(
            glob.strip().strip(QUOTES)
            for glob in fields.get("globs", "").split(",")
            if glob.strip().strip(QUOTES)
        )
        always = fields.get("alwaysApply", "").lower() == "true"
        return Rule(name=path.stem, source=text, body=body, globs=globs, always=always)

    @staticmethod
    def _fields(frontmatter: str) -> dict[str, str]:
        fields: dict[str, str] = {}
        for line in frontmatter.splitlines():
            key, separator, value = line.partition(":")
            if separator:
                fields[key.strip()] = value.strip()
        return fields
