"""Mirror a skill folder into a target without deleting whole directories."""

import logging
import shutil
import stat
from pathlib import Path

from agent_kit.utils import retry_on_permission_error

logger = logging.getLogger(__name__)

SKIPPED_DIRS = frozenset({"__pycache__"})
SKIPPED_SUFFIXES = frozenset({".pyc"})


class FolderSync:
    """Makes a destination folder match a source folder, file by file.

    Whole folders are never removed, so a directory that Windows locks for a moment
    cannot leave a half-copied skill behind.
    """

    def files_of(self, src: Path) -> set[Path]:
        """List the files that get mirrored, relative to ``src``.

        :param src: The source folder.
        :return: Relative paths, without Python caches.
        """
        return {
            path.relative_to(src)
            for path in src.rglob("*")
            if path.is_file()
            and not SKIPPED_DIRS.intersection(path.parts)
            and path.suffix not in SKIPPED_SUFFIXES
        }

    def sync(self, src: Path, dest: Path) -> None:
        """Copy every source file over, then remove files the source no longer has.

        :param src: The source folder.
        :param dest: The destination folder; created when missing.
        :raises PermissionError: If a file stays locked after every retry.
        """
        wanted = self.files_of(src)
        for rel in sorted(wanted):
            self._copy(src / rel, dest / rel)
        if dest.is_dir():
            self._remove_stale(dest, wanted)
        logger.debug("synced %s -> %s (%d files)", src, dest, len(wanted))

    def _copy(self, src: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_file():
            self._make_writable(dest)
        retry_on_permission_error(lambda: shutil.copy2(src, dest))

    def _remove_stale(self, dest: Path, wanted: set[Path]) -> None:
        for path in sorted(dest.rglob("*"), reverse=True):  # children before parents
            if path.is_file() and path.relative_to(dest) not in wanted:
                self._make_writable(path)
                retry_on_permission_error(path.unlink)
            elif path.is_dir() and not any(path.iterdir()):
                self._remove_empty_dir(path)

    @staticmethod
    def _remove_empty_dir(path: Path) -> None:
        try:
            path.rmdir()
        except OSError:
            logger.debug("kept locked empty folder %s", path)

    @staticmethod
    def _make_writable(path: Path) -> None:
        path.chmod(path.stat().st_mode | stat.S_IWUSR)
