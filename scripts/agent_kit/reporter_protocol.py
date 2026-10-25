"""The interface the installer and commands use to report progress to the user."""

from typing import Protocol


class ReporterProtocol(Protocol):
    """Receives user-facing progress lines, warnings, and notes."""

    def action(self, action: str, path: str, note: str = "") -> None:
        """Report one change to a file.

        :param action: A short verb such as ``write``, ``skip``, or ``mcp``.
        :param path: The file, relative to the target.
        :param note: Optional detail, such as a server name.
        """

    def info(self, message: str) -> None:
        """Report a plain line.

        :param message: The text to show.
        """

    def warn(self, message: str) -> None:
        """Report something the user should fix by hand.

        :param message: The warning text.
        """

    def error(self, message: str) -> None:
        """Report why a command failed.

        :param message: The error text.
        """
