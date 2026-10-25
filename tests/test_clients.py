"""Tests for the client adapters, the Codex TOML table, and the registry."""

import json
import tomllib
from pathlib import Path

import pytest
from utils import write

from agent_kit.clients import (
    ClaudeAdapter,
    ClientRegistry,
    CodexAdapter,
    CodexMcpTable,
    CursorAdapter,
    OpenCodeAdapter,
)
from agent_kit.errors import InstallError
from agent_kit.files import TargetWriter
from agent_kit.models import McpServer, RemoteServer, Rule, StdioServer

ALWAYS = Rule(
    name="always",
    source="---\nalwaysApply: true\n---\n# A\n",
    body="# A\n",
    always=True,
)
SCOPED = Rule(name="scoped", source="src", body="# S\n", globs=("*.py",))
SERVERS: dict[str, McpServer] = {
    "local": StdioServer(
        command="npx", args=("-y", "p@1"), env={"TOKEN": "${env:TOKEN}"}
    ),
    "remote": RemoteServer(
        url="https://x.test/mcp", headers={"Authorization": "Bearer ${env:KEY}"}
    ),
}


def read_json(path: Path) -> dict[str, object]:
    """Load a JSON object from disk.

    :param path: The file.
    :return: The parsed object.
    """
    data: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    return data


def test_detect_lists_present_markers(target: Path) -> None:
    (target / ".claude").mkdir()
    write(target / "CLAUDE.md", "")
    assert ClaudeAdapter().detect(target) == [".claude", "CLAUDE.md"]
    assert CursorAdapter().detect(target) == []


def test_cursor_rules_and_mcp(writer: TargetWriter) -> None:
    adapter = CursorAdapter()
    adapter.install_rules(writer, [SCOPED])
    adapter.install_mcp(writer, SERVERS)
    assert (writer.root / ".cursor/rules/scoped.mdc").read_text(
        encoding="utf-8"
    ) == "src"
    servers = read_json(writer.root / ".cursor/mcp.json")["mcpServers"]
    assert servers == {
        "local": {
            "command": "npx",
            "args": ["-y", "p@1"],
            "env": {"TOKEN": "${env:TOKEN}"},
        },
        "remote": {
            "url": "https://x.test/mcp",
            "headers": {"Authorization": "Bearer ${env:KEY}"},
        },
    }


def test_claude_rules_scope_with_paths(writer: TargetWriter) -> None:
    ClaudeAdapter().install_rules(writer, [ALWAYS, SCOPED])
    assert (writer.root / ".claude/rules/always.md").read_text(
        encoding="utf-8"
    ) == "# A\n"
    scoped = (writer.root / ".claude/rules/scoped.md").read_text(encoding="utf-8")
    assert scoped == '---\npaths:\n  - "*.py"\n---\n\n# S\n'


def test_claude_mcp_rewrites_env_and_types_remote(writer: TargetWriter) -> None:
    ClaudeAdapter().install_mcp(writer, SERVERS)
    servers = read_json(writer.root / ".mcp.json")["mcpServers"]
    assert isinstance(servers, dict)
    assert servers["local"]["env"] == {"TOKEN": "${TOKEN}"}
    assert servers["remote"]["type"] == "http"
    assert servers["remote"]["headers"]["Authorization"] == "Bearer ${KEY}"


def test_claude_finish_links_agents_md(writer: TargetWriter) -> None:
    adapter = ClaudeAdapter()
    adapter.finish(writer, installs_agents_md=False)
    assert not (writer.root / "CLAUDE.md").exists()
    adapter.finish(writer, installs_agents_md=True)
    assert (writer.root / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n"


def test_claude_finish_warns_on_existing_claude_md(writer: TargetWriter) -> None:
    write(writer.root / "CLAUDE.md", "# mine\n")
    ClaudeAdapter().finish(writer, installs_agents_md=True)
    assert writer.warnings and "@AGENTS.md" in writer.warnings[0]


def test_opencode_preflight_rejects_jsonc_only(target: Path) -> None:
    write(target / "opencode.jsonc", "{}")
    with pytest.raises(InstallError):
        OpenCodeAdapter().preflight(target)
    write(target / "opencode.json", "{}")
    OpenCodeAdapter().preflight(target)


def test_opencode_rules_and_mcp(writer: TargetWriter) -> None:
    adapter = OpenCodeAdapter()
    adapter.install_rules(writer, [SCOPED])
    adapter.install_mcp(writer, SERVERS)
    note = (writer.root / ".opencode/rules/scoped.md").read_text(encoding="utf-8")
    assert note.startswith("_Applies when working on files matching: `*.py`._")
    config = read_json(writer.root / "opencode.json")
    assert config["instructions"] == [".opencode/rules/*.md"]
    assert config["$schema"] == "https://opencode.ai/config.json"
    mcp = config["mcp"]
    assert isinstance(mcp, dict)
    assert mcp["local"] == {
        "type": "local",
        "command": ["npx", "-y", "p@1"],
        "environment": {"TOKEN": "{env:TOKEN}"},
        "enabled": True,
    }
    assert mcp["remote"]["headers"] == {"Authorization": "Bearer {env:KEY}"}


def test_codex_rules_block_is_idempotent(writer: TargetWriter) -> None:
    write(writer.root / "AGENTS.md", "# Agents\n")
    adapter = CodexAdapter()
    adapter.install_rules(writer, [ALWAYS, SCOPED])
    adapter.install_rules(writer, [ALWAYS])
    text = (writer.root / "AGENTS.md").read_text(encoding="utf-8")
    assert text.startswith("# Agents\n")
    assert text.count("agent-kit:rules:begin") == 1
    assert "<!-- agent-kit:rule scoped -->" in text
    assert "## A" in text  # headings demoted


def test_codex_mcp_keeps_user_servers(writer: TargetWriter) -> None:
    write(writer.root / ".codex/config.toml", '[mcp_servers.local]\ncommand = "mine"\n')
    adapter = CodexAdapter()
    adapter.install_mcp(writer, SERVERS)
    adapter.install_mcp(writer, SERVERS)
    config = tomllib.loads(
        (writer.root / ".codex/config.toml").read_text(encoding="utf-8")
    )
    assert config["mcp_servers"]["local"] == {"command": "mine"}
    assert config["mcp_servers"]["remote"]["bearer_token_env_var"] == "KEY"


def test_codex_notes_only_with_servers() -> None:
    assert CodexAdapter().notes(SERVERS)
    assert CodexAdapter().notes({}) == []


def test_codex_table_renders_env_passthrough_and_literal() -> None:
    warnings: list[str] = []
    server = StdioServer(
        command="c", env={"A": "${env:A}", "B": "b"}, args=("${env:X}",)
    )
    toml = CodexMcpTable().render("s", server, warnings.append)
    parsed = tomllib.loads(toml)["mcp_servers"]["s"]
    assert parsed["env_vars"] == ["A"]
    assert parsed["env"] == {"B": "b"}
    assert warnings == ["s: Codex does not expand ${env:...} in args"]


def test_registry_names_get_and_detect(target: Path) -> None:
    registry = ClientRegistry()
    assert registry.names() == ["cursor", "claude", "opencode", "codex"]
    assert isinstance(registry.get("codex"), CodexAdapter)
    with pytest.raises(InstallError):
        registry.get("vim")
    (target / ".codex").mkdir()
    assert registry.detect(target) == {"codex": [".codex"]}
