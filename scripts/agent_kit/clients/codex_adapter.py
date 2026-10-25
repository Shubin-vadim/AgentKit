"""Codex: ``.agents/skills``, a rules block in ``AGENTS.md``, ``.codex/config.toml``."""

import re
from typing import ClassVar

from agent_kit.clients.client_adapter import AGENTS_MD, ClientAdapter
from agent_kit.clients.codex_mcp_table import CodexMcpTable
from agent_kit.files import ManagedBlock, TargetWriter
from agent_kit.models import McpServer, Rule

RULES_HEADING = "## Rules installed by agent-kit"
RULE_MARKER = "<!-- agent-kit:rule {} -->"
SERVER_HEADER = re.compile(r'^\s*\[mcp_servers\.("[^"]+"|[A-Za-z0-9_-]+)')
TABLE_HEADER = "["


class CodexAdapter(ClientAdapter):
    """Keeps agent-kit's rules and servers in managed blocks; user entries stay."""

    name: ClassVar[str] = "codex"
    label: ClassVar[str] = "Codex"
    markers: ClassVar[tuple[str, ...]] = (".codex",)
    skills_dir: ClassVar[str] = ".agents/skills"
    config_file: ClassVar[str] = ".codex/config.toml"
    rules_block: ClassVar[ManagedBlock] = ManagedBlock(
        begin="<!-- agent-kit:rules:begin -->", end="<!-- agent-kit:rules:end -->"
    )
    mcp_block: ClassVar[ManagedBlock] = ManagedBlock(
        begin="# >>> agent-kit mcp (managed; edit the kit, not this block)",
        end="# <<< agent-kit mcp",
    )

    def __init__(self, table: CodexMcpTable | None = None) -> None:
        self._table = table or CodexMcpTable()

    def install_rules(self, writer: TargetWriter, rules: list[Rule]) -> None:
        """Keep one marked section per rule inside a managed block of ``AGENTS.md``.

        :param writer: Writer bound to the target.
        :param rules: Rules to install.
        """
        path = writer.root / AGENTS_MD
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        sections = self._rule_sections(self.rules_block.inner(text))
        for rule in rules:
            if rule.name in sections and not writer.force:
                writer.report("skip", path, f"rule {rule.name}")
                continue
            writer.report(
                "replace" if rule.name in sections else "rule",
                path,
                f"rule {rule.name}",
            )
            sections[rule.name] = rule.scope_note() + rule.demoted_body().strip()
        body = "\n\n".join(f"{RULE_MARKER.format(n)}\n{t}" for n, t in sections.items())
        writer.write_text(
            path, self.rules_block.put(text, f"{RULES_HEADING}\n\n{body}")
        )

    @staticmethod
    def _rule_sections(block: str) -> dict[str, str]:
        prefix, suffix = RULE_MARKER.split("{}")
        marker = re.escape(prefix) + r"(\S+)" + re.escape(suffix)
        parts = re.split(marker, block)  # [preamble, name1, text1, name2, text2, ...]
        return {
            name: text.strip()
            for name, text in zip(parts[1::2], parts[2::2], strict=True)
        }

    def install_mcp(self, writer: TargetWriter, servers: dict[str, McpServer]) -> None:
        """Keep agent-kit's servers in a managed block of ``.codex/config.toml``.

        :param writer: Writer bound to the target.
        :param servers: Servers to add, by name.
        """
        path = writer.root / self.config_file
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        user_defined = set(self._server_tables(self.mcp_block.outside(text)))
        managed = self._server_tables(self.mcp_block.inner(text))
        for name, server in servers.items():
            if name in user_defined:
                writer.report(
                    "skip", path, f"{name}, defined outside the agent-kit block"
                )
            elif name in managed and not writer.force:
                writer.report("skip", path, name)
            else:
                writer.report("replace" if name in managed else "mcp", path, name)
                managed[name] = self._table.render(name, server, writer.warn)
        writer.write_text(path, self.mcp_block.put(text, "\n\n".join(managed.values())))

    @staticmethod
    def _server_tables(toml: str) -> dict[str, str]:
        tables: dict[str, list[str]] = {}
        current: str | None = None
        for line in toml.splitlines():
            match = SERVER_HEADER.match(line)
            if match:
                current = match.group(1).strip('"')
                tables.setdefault(current, [])
            elif line.lstrip().startswith(TABLE_HEADER):
                current = None  # a table that is not an MCP server
            if current is not None:
                tables[current].append(line)
        return {name: "\n".join(lines).strip() for name, lines in tables.items()}

    def notes(self, servers: dict[str, McpServer]) -> list[str]:
        """Remind the user that Codex ignores project config until it is trusted.

        :param servers: The servers that were installed.
        :return: The reminder when servers were installed.
        """
        return (
            [f"Codex reads {self.config_file} only in trusted projects."]
            if servers
            else []
        )
