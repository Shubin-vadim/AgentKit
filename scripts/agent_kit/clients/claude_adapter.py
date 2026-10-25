"""Claude Code: ``.claude/skills``, ``.claude/rules/*.md``, ``.mcp.json``."""

from typing import ClassVar

from agent_kit.clients.client_adapter import AGENTS_MD, ClientAdapter
from agent_kit.files import JsonObject, TargetWriter
from agent_kit.models import McpServer, RemoteServer, Rule
from agent_kit.utils import rewrite_env_refs

MCP_KEY = "mcpServers"
ENV_REF_REPLACEMENT = r"${\1}"
REMOTE_TYPE = "http"


class ClaudeAdapter(ClientAdapter):
    """Scopes rules with ``paths`` and links ``CLAUDE.md`` to ``AGENTS.md``."""

    name: ClassVar[str] = "claude"
    label: ClassVar[str] = "Claude Code"
    markers: ClassVar[tuple[str, ...]] = (".claude", "CLAUDE.md", ".mcp.json")
    skills_dir: ClassVar[str] = ".claude/skills"
    rules_dir: ClassVar[str] = ".claude/rules"
    mcp_file: ClassVar[str] = ".mcp.json"
    memory_file: ClassVar[str] = "CLAUDE.md"
    agents_import: ClassVar[str] = "@" + AGENTS_MD

    def install_rules(self, writer: TargetWriter, rules: list[Rule]) -> None:
        """Write ``.claude/rules/<name>.md``; scoped rules get ``paths`` frontmatter.

        :param writer: Writer bound to the target.
        :param rules: Rules to install.
        """
        for rule in rules:
            head = ""
            if rule.scope:
                paths = "".join(f'  - "{glob}"\n' for glob in rule.scope)
                head = f"---\npaths:\n{paths}---\n\n"
            writer.write_unless_present(
                writer.root / self.rules_dir / f"{rule.name}.md", head + rule.body
            )

    def install_mcp(self, writer: TargetWriter, servers: dict[str, McpServer]) -> None:
        """Merge the servers into ``.mcp.json`` with ``${NAME}`` references.

        :param writer: Writer bound to the target.
        :param servers: Servers to add, by name.
        """
        entries = {name: self._entry(server) for name, server in servers.items()}
        writer.merge_entries(writer.root / self.mcp_file, MCP_KEY, entries)

    @staticmethod
    def _entry(server: McpServer) -> JsonObject:
        data = server.model_dump(mode="json", exclude_defaults=True)
        entry: JsonObject = {}
        if isinstance(server, RemoteServer):
            entry["type"] = REMOTE_TYPE  # Claude Code reads an untyped entry as stdio
        for key, value in data.items():
            entry[key] = rewrite_env_refs(value, ENV_REF_REPLACEMENT)
        return entry

    def finish(self, writer: TargetWriter, installs_agents_md: bool) -> None:
        """Create ``CLAUDE.md`` importing ``AGENTS.md``.

        Claude Code before 2.1.277 reads only ``CLAUDE.md``.

        :param writer: Writer bound to the target.
        :param installs_agents_md: Whether this installation provides ``AGENTS.md``.
        """
        if not (installs_agents_md or (writer.root / AGENTS_MD).is_file()):
            return
        path = writer.root / self.memory_file
        if not path.is_file():
            writer.report("write", path, f"imports {AGENTS_MD}")
            writer.write_text(path, self.agents_import + "\n")
        elif self.agents_import not in path.read_text(encoding="utf-8"):
            writer.warn(
                f"{self.memory_file} exists without '{self.agents_import}'; "
                f"add that line so Claude Code also reads {AGENTS_MD}"
            )
