# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.9,<3"]
# ///
"""Write ``docs/skills.md`` and ``docs/profiles.md`` from the public library.

Run from anywhere with ``uv run website/build_catalog.py`` before building the site.
"""

import sys
from pathlib import Path

WEBSITE_DIR = Path(__file__).resolve().parent
KIT_ROOT = WEBSITE_DIR.parent
sys.path[:0] = [str(KIT_ROOT / "scripts"), str(WEBSITE_DIR)]  # agent_kit, site_catalog

from agent_kit import AppError  # noqa: E402  (needs the path above)
from agent_kit.library import Library  # noqa: E402
from site_catalog import CatalogReader, PageRenderer, ReadmeTables  # noqa: E402

DOCS_DIR = WEBSITE_DIR / "docs"
README = KIT_ROOT / "README.md"


def main() -> int:
    """Generate both catalog pages.

    :return: ``0`` on success, ``1`` when the kit or README cannot be read.
    """
    try:
        library = Library([KIT_ROOT])  # this repository only
        reader = CatalogReader(library, ReadmeTables(README.read_text("utf-8")))
        renderer = PageRenderer()
        pages = {
            "skills.md": renderer.skills_page(reader.skills()),
            "profiles.md": renderer.profiles_page(reader.profiles()),
        }
    except AppError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    for name, text in pages.items():
        (DOCS_DIR / name).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {(DOCS_DIR / name).relative_to(KIT_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
