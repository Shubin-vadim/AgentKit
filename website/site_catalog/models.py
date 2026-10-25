"""Models for the generated website pages: skills, their sources, and profiles."""

from pydantic import BaseModel, ConfigDict


class SkillSource(BaseModel):
    """Where a vendored skill comes from, as listed in the README."""

    model_config = ConfigDict(frozen=True)

    label: str
    url: str
    license: str


class SourceRule(BaseModel):
    """One README "Skill sources" row: which skill names it covers, and the source."""

    model_config = ConfigDict(frozen=True)

    names: tuple[str, ...]
    prefixes: tuple[str, ...] = ()
    excluded: tuple[str, ...] = ()
    source: SkillSource

    def covers(self, name: str) -> bool:
        """Tell whether this row describes a skill.

        :param name: A skill folder name.
        :return: ``True`` for a listed name or a ``prefix-*`` match not excluded.
        """
        if name in self.excluded:
            return False
        return name in self.names or name.startswith(self.prefixes)


class SkillEntry(BaseModel):
    """One skill as the catalog shows it."""

    model_config = ConfigDict(frozen=True)

    name: str
    summary: str
    group: tuple[str, ...]
    profiles: tuple[str, ...] = ()
    source: SkillSource | None = None


class ProfileEntry(BaseModel):
    """One profile as the catalog shows it."""

    model_config = ConfigDict(frozen=True)

    name: str
    summary: str
    skills: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()
    mcp: tuple[str, ...] = ()
    templates: tuple[str, ...] = ()
