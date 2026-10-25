"""Read ``profiles/*.yaml`` install lists."""

import re
from pathlib import Path

from agent_kit.models import Profile, TemplateSpec

LIST_KEY = re.compile(r"^[A-Za-z][\w-]*:\s*$")
SCALAR_KEY = re.compile(r"^[A-Za-z][\w-]*:")
LIST_ITEM = re.compile(r"^\s*-\s+")


class ProfileParser:
    """Parses the flat ``key:`` + ``- item`` lists that profiles use."""

    def parse(self, path: Path) -> Profile:
        """Read one profile file.

        :param path: A ``profiles/<name>.yaml`` file.
        :return: The profile, named after the file.
        """
        lists = self._lists(path.read_text(encoding="utf-8"))
        return Profile(
            name=path.stem,
            path=path,
            skills=tuple(lists.get("skills", [])),
            rules=tuple(lists.get("rules", [])),
            mcp=tuple(lists.get("mcp", [])),
            templates=tuple(TemplateSpec.parse(s) for s in lists.get("templates", [])),
        )

    @staticmethod
    def _lists(text: str) -> dict[str, list[str]]:
        lists: dict[str, list[str]] = {}
        current: list[str] | None = None
        for line in text.splitlines():
            if LIST_KEY.match(line):
                current = lists.setdefault(line.split(":", 1)[0], [])
            elif SCALAR_KEY.match(line):
                current = None
            elif current is not None and LIST_ITEM.match(line):
                current.append(LIST_ITEM.sub("", line).strip())
        return lists
