"""Read ``mcp/**/*.json`` fragments into server models."""

import json
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from agent_kit.errors import LibraryError
from agent_kit.models import McpServer

SERVERS_KEY = "mcpServers"


class McpFragmentLoader:
    """Validates an MCP fragment (``{name: server}``) against the server models."""

    def __init__(self) -> None:
        self._adapter: TypeAdapter[dict[str, McpServer]] = TypeAdapter(
            dict[str, McpServer]
        )

    def load(self, path: Path) -> dict[str, McpServer]:
        """Read one fragment.

        :param path: An ``mcp/<name>/<name>.json`` file.
        :return: The servers it defines, by name.
        :raises LibraryError: If the file is not valid JSON or a server has neither
            ``command`` nor ``url``.
        """
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            servers = data.get(SERVERS_KEY, data) if isinstance(data, dict) else data
            return self._adapter.validate_python(servers)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise LibraryError(f"Invalid MCP fragment {path}: {exc}") from exc
