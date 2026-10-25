"""OpenCode: ``.opencode/skills``, ``.opencode/rules/*.md``, ``opencode.json``."""

from pathlib import Path
from typing import ClassVar

from agent_kit.clients.client_adapter import ClientAdapter
from agent_kit.errors import InstallError
from agent_kit.files import JsonObject, TargetWriter
from agent_kit.models import McpServer, RemoteServer, Rule
from agent_kit.utils import JsonValue, rewrite_env_refs

ENV_REF_REPLACEMENT = r"{env:\1}"
SCHEMA_URL = "https://opencode.ai/config.json"
INSTRUCTIONS_KEY = "instructions"
MCP_KEY = "mcp"


class OpenCodeAdapter(ClientAdapter):
    """Lists rule files in ``instructions`` and writes typed ``mcp`` entries."""

    name: ClassVar[str] = "opencode"
    label: ClassVar[str] = "OpenCode"
    markers: ClassVar[tuple[str, ...]] = (
        ".opencode",
        "opencode.json",
        "opencode.jsonc",
    )
    skills_dir: ClassVar[str] = ".opencode/skills"
    rules_dir: ClassVar[str] = ".opencode/rules"
    config_file: ClassVar[str] = "opencode.json"
    commented_config_file: ClassVar[str] = "opencode.jsonc"

    def preflight(self, target: Path) -> None:
        """Refuse a project whose only config is ``opencode.jsonc``.

        Its comments could not be preserved.

        :param target: The project directory.
        :raises InstallError: If ``opencode.jsonc`` exists without ``opencode.json``.
        """
        if (target / self.commented_config_file).is_file() and not (
            target / self.config_file
        ).is_file():
            raise InstallError(
                f"{target / self.commented_config_file} found; this installer "
                f"only edits {self.config_file}. Rename it or merge by hand."
            )

    def install_rules(self, writer: TargetWriter, rules: list[Rule]) -> None:
        """Write ``.opencode/rules/<name>.md`` and list them in ``instructions``.

        OpenCode cannot scope rules by path, so the scope becomes a note in the file.

        :param writer: Writer bound to the target.
        :param rules: Rules to install.
        """
        for rule in rules:
            path = writer.root / self.rules_dir / f"{rule.name}.md"
            writer.write_unless_present(path, rule.scope_note() + rule.body)
        self._list_rules(writer)

    def _list_rules(self, writer: TargetWriter) -> None:
        path = writer.root / self.config_file
        data = writer.read_json(path)
        instructions = data.setdefault(INSTRUCTIONS_KEY, [])
        glob = f"{self.rules_dir}/*.md"
        if isinstance(instructions, list) and glob not in instructions:
            instructions.append(glob)
            writer.report("update", path, INSTRUCTIONS_KEY)
            writer.write_json(path, {"$schema": SCHEMA_URL, **data})

    def install_mcp(self, writer: TargetWriter, servers: dict[str, McpServer]) -> None:
        """Merge the servers into ``opencode.json`` under ``mcp``.

        :param writer: Writer bound to the target.
        :param servers: Servers to add, by name.
        """
        path = writer.root / self.config_file
        writer.set_defaults(path, {"$schema": SCHEMA_URL})
        entries = {name: self._entry(server) for name, server in servers.items()}
        writer.merge_entries(path, MCP_KEY, entries)

    @staticmethod
    def _entry(server: McpServer) -> JsonObject:
        entry: JsonObject
        if isinstance(server, RemoteServer):
            entry = {"type": "remote", "url": server.url}
            if server.headers:
                entry["headers"] = rewrite_env_refs(
                    dict(server.headers), ENV_REF_REPLACEMENT
                )
        else:
            command: list[JsonValue] = [server.command, *server.args]
            entry = {
                "type": "local",
                "command": rewrite_env_refs(command, ENV_REF_REPLACEMENT),
            }
            if server.env:
                entry["environment"] = rewrite_env_refs(
                    dict(server.env), ENV_REF_REPLACEMENT
                )
        entry["enabled"] = True
        return entry
