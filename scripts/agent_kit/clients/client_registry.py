"""The registry of supported agent clients."""

from pathlib import Path

from agent_kit.clients.claude_adapter import ClaudeAdapter
from agent_kit.clients.client_adapter import ClientAdapter
from agent_kit.clients.codex_adapter import CodexAdapter
from agent_kit.clients.cursor_adapter import CursorAdapter
from agent_kit.clients.opencode_adapter import OpenCodeAdapter
from agent_kit.errors import InstallError


class ClientRegistry:
    """Looks up client adapters by name and detects which ones a project uses."""

    def __init__(self, adapters: list[ClientAdapter] | None = None) -> None:
        default = [CursorAdapter(), ClaudeAdapter(), OpenCodeAdapter(), CodexAdapter()]
        self._adapters = {adapter.name: adapter for adapter in adapters or default}

    def names(self) -> list[str]:
        """List the supported client names.

        :return: Names in registration order.
        """
        return list(self._adapters)

    def get(self, name: str) -> ClientAdapter:
        """Find an adapter by client name.

        :param name: A client name such as ``claude``.
        :return: The adapter.
        :raises InstallError: If no client has that name.
        """
        if name not in self._adapters:
            raise InstallError(
                f"Unknown client '{name}'. Use one of: {', '.join(self._adapters)}."
            )
        return self._adapters[name]

    def detect(self, target: Path) -> dict[str, list[str]]:
        """Find clients whose marker files or folders exist in a project.

        :param target: The project directory.
        :return: Client names mapped to the markers found.
        """
        found = {
            name: adapter.detect(target) for name, adapter in self._adapters.items()
        }
        return {name: markers for name, markers in found.items() if markers}
