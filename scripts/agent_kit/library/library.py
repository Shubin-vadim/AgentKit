"""Find assets by name across the kit's asset folders."""

import logging
from functools import cached_property
from pathlib import Path

from agent_kit.errors import LibraryError
from agent_kit.library.profile_parser import ProfileParser
from agent_kit.models import AssetKind, KitLayout, Profile, Selection
from agent_kit.utils import unique

logger = logging.getLogger(__name__)

SKILL = AssetKind(
    label="skill", folder="skills", pattern="SKILL.md", named_by_folder=True
)
RULE = AssetKind(label="rule", folder="rules", pattern="*.mdc")
MCP = AssetKind(label="MCP fragment", folder="mcp", pattern="*.json")
PROFILE = AssetKind(label="profile", folder="profiles", pattern="*.yaml")
TEMPLATES_FOLDER = "templates"
CORE_PROFILE = "core"

type AssetIndex = dict[str, list[Path]]


class Library:
    """The kit root and any further asset folders, searched together by name."""

    def __init__(self, roots: list[Path], parser: ProfileParser | None = None) -> None:
        self.roots = roots
        self._parser = parser or ProfileParser()

    @classmethod
    def discover(cls, layout: KitLayout) -> "Library":
        """Collect the kit root and the layout's extra asset folders.

        :param layout: Where the kit lives.
        :return: A library over every root, kit first.
        :raises LibraryError: If an extra folder is not a directory.
        """
        roots = [layout.root]
        for candidate in layout.library_dirs:
            if not candidate.is_dir():
                raise LibraryError(f"Library is not an existing directory: {candidate}")
            roots.append(candidate.resolve())
        logger.debug("library roots: %s", roots)
        return cls(unique(roots))

    @property
    def extra_roots(self) -> list[Path]:
        """List the libraries added to the kit.

        :return: Every root except the kit itself.
        """
        return self.roots[1:]

    def contains(self, path: Path) -> bool:
        """Tell whether a path is a library root or lies inside one.

        :param path: An absolute path.
        :return: ``True`` for any library root or anything under one.
        """
        return any(path == root or root in path.parents for root in self.roots)

    def index(self, kind: AssetKind) -> AssetIndex:
        """Map every asset name of a kind to the files that define it.

        :param kind: Which assets to index.
        :return: Names to paths; more than one path means a duplicate.
        """
        return self._indexes[kind.folder]

    def _scan(self, kind: AssetKind) -> AssetIndex:
        found: AssetIndex = {}
        for root in self.roots:
            base = root / kind.folder
            if base.is_dir():
                for path in sorted(base.rglob(kind.pattern)):
                    found.setdefault(kind.name_of(path), []).append(path)
        return found

    @cached_property
    def _indexes(self) -> dict[str, AssetIndex]:
        return {kind.folder: self._scan(kind) for kind in (SKILL, RULE, MCP, PROFILE)}

    def _one(self, kind: AssetKind, name: str) -> Path:
        paths = self._indexes[kind.folder].get(name, [])
        if not paths:
            raise LibraryError(f"No {kind.label} named '{name}' in {self.roots}.")
        if len(paths) > 1:
            raise LibraryError(f"Duplicate {kind.label} '{name}': {paths}.")
        return paths[0]

    def skill(self, name: str) -> Path:
        """Find a skill by its folder name.

        :param name: A skill folder name.
        :return: The skill folder.
        :raises LibraryError: If the skill is missing or defined twice.
        """
        return self._one(SKILL, name).parent

    def rule(self, name: str) -> Path:
        """Find a rule by its file name.

        :param name: A rule file name without ``.mdc``.
        :return: The rule file.
        :raises LibraryError: If the rule is missing or defined twice.
        """
        return self._one(RULE, name)

    def mcp_fragment(self, name: str) -> Path:
        """Find an MCP fragment by its file name.

        :param name: An MCP fragment file name without ``.json``.
        :return: The fragment file.
        :raises LibraryError: If the fragment is missing or defined twice.
        """
        return self._one(MCP, name)

    def template_candidates(self, rel: str) -> list[Path]:
        """List every library file at a template path.

        :param rel: A path under ``templates/``.
        :return: Matching files; more than one is a conflict.
        """
        candidates = [root / TEMPLATES_FOLDER / rel for root in self.roots]
        return [path for path in candidates if path.is_file()]

    def template(self, rel: str) -> Path:
        """Find the one template file at a path.

        :param rel: A path under ``templates/``.
        :return: The single template file.
        :raises LibraryError: If the template is missing or exists in several libraries.
        """
        paths = self.template_candidates(rel)
        if len(paths) != 1:
            state = "missing" if not paths else f"in {len(paths)} libraries"
            raise LibraryError(f"Template '{TEMPLATES_FOLDER}/{rel}' is {state}.")
        return paths[0]

    def profile_names(self) -> list[str]:
        """List the available profiles.

        :return: Every profile name, sorted.
        """
        return sorted(self._indexes[PROFILE.folder])

    def profile(self, name: str) -> Profile:
        """Load a profile by name.

        :param name: A profile name.
        :return: The parsed profile.
        :raises LibraryError: If no profile has that name, or two do.
        """
        if name not in self._indexes[PROFILE.folder]:
            available = ", ".join(self.profile_names())
            raise LibraryError(f"Unknown profile '{name}'. Available: {available}.")
        return self._parser.parse(self._one(PROFILE, name))

    def select(self, names: list[str], include_core: bool) -> Selection:
        """Merge the install lists of several profiles.

        :param names: Profile names in priority order.
        :param include_core: Add ``core`` first when it is not listed.
        :return: The de-duplicated selection.
        :raises LibraryError: If a profile does not exist.
        """
        names = unique(names)
        if include_core and CORE_PROFILE not in names:
            names.insert(0, CORE_PROFILE)
        profiles = [self.profile(name) for name in names]
        return Selection(
            profiles=tuple(names),
            skills=tuple(unique(s for p in profiles for s in p.skills)),
            rules=tuple(unique(r for p in profiles for r in p.rules)),
            mcp=tuple(unique(m for p in profiles for m in p.mcp)),
            templates=tuple(unique(t for p in profiles for t in p.templates)),
        )
