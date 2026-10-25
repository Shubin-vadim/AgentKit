"""The Strategy interface every agent client implements."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar

from agent_kit.files import TargetWriter
from agent_kit.models import McpServer, Rule

AGENTS_MD = "AGENTS.md"


class ClientAdapter(ABC):
    """Writes skills, rules, and MCP servers in the layout one agent client reads."""

    name: ClassVar[str]
    label: ClassVar[str]
    markers: ClassVar[tuple[str, ...]]
    skills_dir: ClassVar[str]

    def detect(self, target: Path) -> list[str]:
        """List the markers of this client present in a project.

        :param target: The project directory.
        :return: Marker files or folders that exist there.
        """
        return [marker for marker in self.markers if (target / marker).exists()]

    def preflight(self, target: Path) -> None:
        """Refuse a target this client cannot handle, before anything is written.

        :param target: The project directory.
        :raises InstallError: In subclasses, when the target cannot be handled.
        """
        return None  # most clients accept any target

    @abstractmethod
    def install_rules(self, writer: TargetWriter, rules: list[Rule]) -> None:
        """Write rules in this client's format.

        :param writer: Writer bound to the target.
        :param rules: Rules to install.
        """

    @abstractmethod
    def install_mcp(self, writer: TargetWriter, servers: dict[str, McpServer]) -> None:
        """Add MCP servers to this client's configuration.

        :param writer: Writer bound to the target.
        :param servers: Servers to add, by name.
        """

    def finish(self, writer: TargetWriter, installs_agents_md: bool) -> None:
        """Run client-specific steps once templates and rules are in place.

        :param writer: Writer bound to the target.
        :param installs_agents_md: Whether this installation provides ``AGENTS.md``.
        """
        return None  # most clients need no extra step

    def notes(self, servers: dict[str, McpServer]) -> list[str]:
        """Return reminders to print after a successful installation.

        :param servers: The servers that were installed.
        :return: One line per reminder.
        """
        return []
