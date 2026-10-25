"""Client adapters (Strategy) and their registry."""

from agent_kit.clients.claude_adapter import ClaudeAdapter
from agent_kit.clients.client_adapter import AGENTS_MD, ClientAdapter
from agent_kit.clients.client_registry import ClientRegistry
from agent_kit.clients.codex_adapter import CodexAdapter
from agent_kit.clients.codex_mcp_table import CodexMcpTable
from agent_kit.clients.cursor_adapter import CursorAdapter
from agent_kit.clients.opencode_adapter import OpenCodeAdapter

__all__ = [
    "AGENTS_MD",
    "ClaudeAdapter",
    "ClientAdapter",
    "ClientRegistry",
    "CodexAdapter",
    "CodexMcpTable",
    "CursorAdapter",
    "OpenCodeAdapter",
]
