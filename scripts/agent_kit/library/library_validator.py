"""Check a library for duplicate names and dangling profile entries."""

from agent_kit.library.library import MCP, PROFILE, RULE, SKILL, Library
from agent_kit.library.profile_parser import ProfileParser
from agent_kit.models import Profile


class LibraryValidator:
    """Finds every problem that would make an installation fail."""

    def __init__(self, parser: ProfileParser | None = None) -> None:
        self._parser = parser or ProfileParser()

    def problems(self, library: Library) -> list[str]:
        """Validate the whole library.

        :param library: The library to check.
        :return: One message per problem; empty when the library is valid.
        """
        found = self._duplicates(library)
        for paths in library.index(PROFILE).values():
            found += self._dangling(library, self._parser.parse(paths[0]))
        return found

    @staticmethod
    def _duplicates(library: Library) -> list[str]:
        return [
            f"Duplicate {kind.label} name: {name} ({len(paths)} definitions)"
            for kind in (SKILL, RULE, MCP, PROFILE)
            for name, paths in library.index(kind).items()
            if len(paths) > 1
        ]

    @staticmethod
    def _dangling(library: Library, profile: Profile) -> list[str]:
        found = []
        for kind, entries in (
            (SKILL, profile.skills),
            (RULE, profile.rules),
            (MCP, profile.mcp),
        ):
            known = library.index(kind)
            found += [
                f"Profile {profile.name} lists unknown {kind.label} '{entry}'."
                for entry in entries
                if entry not in known
            ]
        for spec in profile.templates:
            count = len(library.template_candidates(spec.src))
            if count != 1:
                state = "missing" if count == 0 else f"in {count} libraries"
                found.append(
                    f"Profile {profile.name} lists template '{spec.src}', {state}."
                )
        return found
