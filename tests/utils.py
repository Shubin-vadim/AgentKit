"""Helpers for building kits and projects on disk in tests."""

import json
import subprocess
from pathlib import Path

ALWAYS_RULE = (
    "---\ndescription: Always\nalwaysApply: true\n---\n\n# Always\n\nBe kind.\n"
)
SCOPED_RULE = (
    '---\ndescription: Py\nglobs: "**/*.py", docs/a.md\n---\n\n# Py\n\nHints.\n'
)
LOCAL_SERVER = {
    "local": {
        "command": "npx",
        "args": ["-y", "pkg@1"],
        "env": {"TOKEN": "${env:TOKEN}", "MODE": "x"},
    }
}
REMOTE_SERVER = {
    "remote": {
        "url": "https://example.test/mcp",
        "headers": {"Authorization": "Bearer ${env:API_KEY}"},
    }
}


def write(path: Path, text: str) -> Path:
    """Create a file with its parent folders.

    :param path: Where to write.
    :param text: File contents.
    :return: The path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def git(path: Path, *args: str) -> None:
    """Run git quietly in a folder.

    :param path: The working directory.
    :param args: Git arguments.
    """
    subprocess.run(["git", "-C", str(path), *args], check=True, capture_output=True)


def build_kit(root: Path) -> Path:
    """Create a minimal kit: two profiles, one skill, two rules, two MCP servers.

    :param root: Where the kit goes.
    :return: The kit root.
    """
    skill = root / "skills" / "group" / "helper"
    write(skill / "SKILL.md", "---\nname: helper\n---\n")
    write(skill / "references" / "notes.md", "notes")
    write(root / "rules" / "core" / "always.mdc", ALWAYS_RULE)
    write(root / "rules" / "py" / "scoped.mdc", SCOPED_RULE)
    write(root / "mcp" / "local" / "local.json", json.dumps(LOCAL_SERVER))
    write(root / "mcp" / "remote" / "remote.json", json.dumps(REMOTE_SERVER))
    write(root / "templates" / "AGENTS.md", "# Agents\n")
    write(
        root / "profiles" / "core.yaml",
        "name: core\nskills:\n  - helper\nrules:\n  - always\nmcp:\n  - local\n"
        "templates:\n  - AGENTS.md\n",
    )
    write(
        root / "profiles" / "extra.yaml",
        "name: extra\nrules:\n  - scoped\nmcp:\n  - remote\n",
    )
    return root
