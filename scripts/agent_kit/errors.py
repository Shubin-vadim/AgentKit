"""Exception hierarchy for agent-kit, rooted in :class:`AppError`.

Exception classes carry no behavior, so they live together as one cohesive family.
"""


class AppError(Exception):
    """Base class for every expected agent-kit failure; the CLI prints it plainly."""


class LibraryError(AppError):
    """The library is missing an asset or has a duplicate or invalid one."""


class InstallError(AppError):
    """An install request cannot be carried out for the given target."""


class ConfigFileError(AppError):
    """A configuration file in the target cannot be read or updated safely."""
