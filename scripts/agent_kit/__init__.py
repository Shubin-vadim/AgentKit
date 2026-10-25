"""agent-kit: install library profiles into projects for any agent client.

Layers, top to bottom: ``cli`` → ``services`` → ``clients`` and ``library`` →
``files``, ``models``, ``utils``. Lower layers never import higher ones.
"""

from agent_kit.cli import KitCli
from agent_kit.errors import (
    AppError,
    ConfigFileError,
    InstallError,
    LibraryError,
)
from agent_kit.models import KitLayout

__all__ = [
    "AppError",
    "ConfigFileError",
    "InstallError",
    "KitCli",
    "KitLayout",
    "LibraryError",
]
