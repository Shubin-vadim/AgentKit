"""Cursor: ``.cursor/skills``, ``.cursor/rules/*.mdc``, ``.cursor/mcp.json``."""

from typing import ClassVar

from agent_kit.clients.client_adapter import ClientAdapter
from agent_kit.files import TargetWriter
from agent_kit.models import McpServer, Rule

MCP_KEY = "mcpServers"


class CursorAdapter(ClientAdapter):
    """Writes ``.mdc`` rules as they are and keeps ``${env:NAME}`` references."""

    name: ClassVar[str] = "cursor"
    label: ClassVar[str] = "Cursor"
    markers: ClassVar[tuple[str, ...]] = (".cursor",)
    skills_dir: ClassVar[str] = ".cursor/skills"
    rules_dir: ClassVar[str] = ".cursor/rules"
    mcp_file: ClassVar[str] = ".cursor/mcp.json"

    def install_rules(self, writer: TargetWriter, rules: list[Rule]) -> None:
        """Copy each rule's ``.mdc`` source unchanged.

        :param writer: Writer bound to the target.
        :param rules: Rules to install.
        """
        for rule in rules:
            path = writer.root / self.rules_dir / f"{rule.name}.mdc"
            writer.write_unless_present(path, rule.source)

    def install_mcp(self, writer: TargetWriter, servers: dict[str, McpServer]) -> None:
        """Merge the servers into ``.cursor/mcp.json``.

        :param writer: Writer bound to the target.
        :param servers: Servers to add, by name.
        """
        entries = {
            name: server.model_dump(mode="json", exclude_defaults=True)
            for name, server in servers.items()
        }
        writer.merge_entries(writer.root / self.mcp_file, MCP_KEY, entries)
