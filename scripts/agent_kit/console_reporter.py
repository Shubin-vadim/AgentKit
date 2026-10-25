"""Console implementation of the reporter used by the command line."""

import sys
from typing import TextIO

ACTION_WIDTH = 9


class ConsoleReporter:
    """Prints progress to stdout and warnings to stderr (the CLI's own output)."""

    def __init__(self, out: TextIO = sys.stdout, err: TextIO = sys.stderr) -> None:
        self._out = out
        self._err = err

    def action(self, action: str, path: str, note: str = "") -> None:
        """Print one change as ``<action> <path> [note]``.

        :param action: A short verb such as ``write`` or ``skip``.
        :param path: The file, relative to the target.
        :param note: Optional detail shown in brackets.
        """
        suffix = f" [{note}]" if note else ""
        print(f"{action:<{ACTION_WIDTH}} {path}{suffix}", file=self._out)

    def info(self, message: str) -> None:
        """Print a plain line to stdout.

        :param message: The text to show.
        """
        print(message, file=self._out)

    def warn(self, message: str) -> None:
        """Print a warning to stderr.

        :param message: The warning text.
        """
        print(f"warning: {message}", file=self._err)

    def error(self, message: str) -> None:
        """Print an error to stderr.

        :param message: The error text.
        """
        print(f"error: {message}", file=self._err)
