"""Every write into a target project goes through :class:`TargetWriter`."""

import json
import logging
from collections.abc import Mapping
from pathlib import Path

from agent_kit.errors import ConfigFileError
from agent_kit.reporter_protocol import ReporterProtocol
from agent_kit.utils import JsonValue

logger = logging.getLogger(__name__)

JSON_INDENT = 2

type JsonObject = dict[str, JsonValue]


class TargetWriter:
    """Writes into one target, honouring ``--dry-run`` and ``--force``."""

    def __init__(
        self, root: Path, reporter: ReporterProtocol, *, force: bool, dry_run: bool
    ) -> None:
        self.root = root
        self.force = force
        self.dry_run = dry_run
        self._reporter = reporter
        self.warnings: list[str] = []

    def report(self, action: str, path: Path, note: str = "") -> None:
        """Report one change, with the path shown relative to the target.

        :param action: A short verb such as ``write`` or ``skip``.
        :param path: The changed file.
        :param note: Optional detail, such as a server name.
        """
        self._reporter.action(action, path.relative_to(self.root).as_posix(), note)

    def warn(self, message: str) -> None:
        """Collect a warning to show once the installation finishes.

        :param message: What the user should fix by hand.
        """
        self.warnings.append(message)

    def write_text(self, path: Path, text: str) -> None:
        """Write a file unless this is a dry run.

        :param path: Destination inside the target.
        :param text: Full file contents.
        """
        if self.dry_run:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        logger.debug("wrote %s (%d chars)", path, len(text))

    def write_unless_present(self, path: Path, text: str) -> None:
        """Create a file; replace an existing one only with ``--force``.

        :param path: Destination inside the target.
        :param text: Full file contents.
        """
        if path.exists() and not self.force:
            self.report("skip", path)
            return
        self.report("replace" if path.exists() else "write", path)
        self.write_text(path, text)

    def read_json(self, path: Path) -> JsonObject:
        """Read a JSON object, or an empty one when the file does not exist.

        :param path: A JSON file inside the target.
        :return: The parsed object.
        :raises ConfigFileError: If the file is not valid JSON or not an object.
        """
        if not path.is_file():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigFileError(
                f"{path} is not valid JSON ({exc}); fix it or move it aside."
            ) from exc
        if not isinstance(data, dict):
            raise ConfigFileError(
                f"{path} must contain a JSON object, found {type(data).__name__}."
            )
        return data

    def write_json(self, path: Path, data: JsonObject) -> None:
        """Write a JSON object with stable formatting.

        :param path: Destination inside the target.
        :param data: The object to write.
        """
        self.write_text(
            path, json.dumps(data, indent=JSON_INDENT, ensure_ascii=False) + "\n"
        )

    def set_defaults(self, path: Path, defaults: JsonObject) -> None:
        """Add top-level keys a JSON file lacks, keeping every existing value.

        :param path: The JSON configuration file.
        :param defaults: Keys and values to add when missing.
        :raises ConfigFileError: If the file exists but cannot be parsed.
        """
        data = self.read_json(path)
        missing = {key: value for key, value in defaults.items() if key not in data}
        if missing:
            self.write_json(path, {**missing, **data})

    def merge_entries(
        self, path: Path, key: str, entries: Mapping[str, JsonValue]
    ) -> None:
        """Add named entries under ``key``; existing names stay unless ``--force``.

        :param path: The JSON configuration file.
        :param key: The object holding the entries, such as ``mcpServers``.
        :param entries: Entries to add, by name.
        :raises ConfigFileError: If the file cannot be parsed or ``key`` is no object.
        """
        data = self.read_json(path)
        section = data.setdefault(key, {})
        if not isinstance(section, dict):
            raise ConfigFileError(
                f"'{key}' in {path} must be an object, found {type(section).__name__}."
            )
        for name, value in entries.items():
            if name in section and not self.force:
                self.report("skip", path, name)
                continue
            self.report("replace" if name in section else "mcp", path, name)
            section[name] = value
        self.write_json(path, data)
