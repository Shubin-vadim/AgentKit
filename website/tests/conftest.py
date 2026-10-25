"""Make ``agent_kit`` and ``site_catalog`` importable and build a tiny kit."""

import sys
from pathlib import Path

import pytest

WEBSITE_DIR = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(WEBSITE_DIR.parent / "scripts"), str(WEBSITE_DIR)]

README = """\
# Kit

## Profiles

| Profile | Adds |
|---------|------|
| `core` | Always added |
| `extra` | Extra things |

## Skill sources

| Skills | Source | License |
|--------|--------|---------|
| `borrowed`, `kit-*` (except `kit-own`) | [up/stream](https://example.test/up) | MIT |

## License
"""


def write(path: Path, text: str) -> None:
    """Create a file with its parent folders.

    :param path: Where to write.
    :param text: File contents.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def skill(root: Path, rel: str, description: str) -> None:
    """Create one skill folder.

    :param root: The kit root.
    :param rel: The folder under ``skills/``.
    :param description: The frontmatter description.
    """
    name = rel.rsplit("/", 1)[-1]
    write(
        root / "skills" / rel / "SKILL.md",
        f"---\nname: {name}\ndescription: >-\n  {description}\n---\n\n# {name}\n",
    )


@pytest.fixture
def kit(tmp_path: Path) -> Path:
    """Build a kit with four skills, two profiles, and a README.

    :param tmp_path: Pytest's temporary folder.
    :return: The kit root.
    """
    root = tmp_path / "kit"
    skill(root, "alpha/borrowed", "Borrowed skill. Use when needed.")
    skill(root, "alpha/kit-one", "First kit skill.")
    skill(root, "alpha/deep/kit-own", "Own skill in a subfolder.")
    skill(root, "beta/solo", "Solo | piped skill.")
    write(root / "profiles" / "core.yaml", "name: core\nskills:\n  - borrowed\n")
    write(
        root / "profiles" / "extra.yaml",
        "name: extra\nskills:\n  - kit-one\n  - borrowed\nrules:\n  - r1\n"
        "templates:\n  - a/b.md => docs/b.md\n",
    )
    write(root / "README.md", README)
    return root
