"""Read-only access to a git checkout through the ``git`` command."""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

UNKNOWN = "unknown"


class GitRepository:
    """Answers questions about one git checkout; degrades gracefully without git."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def _run(self, *args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", "-C", str(self._path), *args],
                capture_output=True,
                text=True,
                check=True,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            logger.debug("git %s failed in %s: %s", " ".join(args), self._path, exc)
            return None
        return result.stdout.strip()

    def revision(self) -> str:
        """Read the checked-out commit.

        :return: The ``HEAD`` commit, or ``"unknown"`` without commits or git.
        """
        return self._run("rev-parse", "--verify", "-q", "HEAD") or UNKNOWN

    def dirty(self) -> str:
        """Tell whether the checkout has uncommitted changes.

        :return: ``"true"``, ``"false"``, or ``"unknown"`` without git.
        """
        status = self._run("status", "--porcelain", "--", ".")
        return UNKNOWN if status is None else str(bool(status)).lower()

    def files(self) -> list[str] | None:
        """List tracked files plus new files that are not ignored.

        :return: Paths relative to the checkout, or ``None`` when git is unavailable.
        """
        output = self._run("ls-files", "--cached", "--others", "--exclude-standard")
        return None if output is None else sorted(set(output.splitlines()))
