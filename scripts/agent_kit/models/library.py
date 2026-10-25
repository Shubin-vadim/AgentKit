"""Models describing the kit layout, library assets, profiles, and selections."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

TEMPLATE_ARROW = " => "


class KitLayout(BaseModel):
    """Where the kit lives and which asset folders are searched after it."""

    model_config = ConfigDict(frozen=True)

    root: Path
    library_dirs: tuple[Path, ...] = ()


class AssetKind(BaseModel):
    """How one kind of asset is stored: its folder, file pattern, and naming."""

    model_config = ConfigDict(frozen=True)

    label: str
    folder: str
    pattern: str
    named_by_folder: bool = False

    def name_of(self, path: Path) -> str:
        """Derive the asset name from one of its files.

        :param path: A file matching :attr:`pattern`.
        :return: The folder name for skills, otherwise the file stem.
        """
        return path.parent.name if self.named_by_folder else path.stem


class TemplateSpec(BaseModel):
    """A profile ``templates:`` entry: ``src => dest``, or one path for both."""

    model_config = ConfigDict(frozen=True)

    src: str
    dest: str

    @classmethod
    def parse(cls, spec: str) -> "TemplateSpec":
        """Build a spec from its profile notation.

        :param spec: ``"a/b.md => c.md"`` or ``"a/b.md"``.
        :return: The parsed spec.
        """
        src, _, dest = spec.partition(TEMPLATE_ARROW)
        return cls(src=src.strip(), dest=(dest or src).strip())


class Profile(BaseModel):
    """One install list from ``profiles/*.yaml``."""

    model_config = ConfigDict(frozen=True)

    name: str
    path: Path
    skills: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()
    mcp: tuple[str, ...] = ()
    templates: tuple[TemplateSpec, ...] = ()


class Selection(BaseModel):
    """Everything a set of profiles asks for, de-duplicated in profile order."""

    model_config = ConfigDict(frozen=True)

    profiles: tuple[str, ...]
    skills: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()
    mcp: tuple[str, ...] = ()
    templates: tuple[TemplateSpec, ...] = ()
