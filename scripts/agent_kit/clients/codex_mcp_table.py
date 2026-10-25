"""Render one MCP server as a ``[mcp_servers.<name>]`` table for Codex."""

import json
import re
from collections.abc import Callable

from agent_kit.models import McpServer, RemoteServer, StdioServer
from agent_kit.utils import ENV_REF_PATTERN

BARE_KEY = re.compile(r"[A-Za-z0-9_-]+")
BEARER_ENV = re.compile(r"Bearer \$\{env:([A-Za-z_][A-Za-z0-9_]*)\}")
AUTHORIZATION = "authorization"

type Warn = Callable[[str], None]


class CodexMcpTable:
    """Turns a server model into TOML for Codex.

    Codex does not expand ``${...}``, so env references become
    ``bearer_token_env_var``, ``env_http_headers``, or ``env_vars``.
    """

    def render(self, name: str, server: McpServer, warn: Warn) -> str:
        """Render the server table and its sub-tables.

        :param name: The server name.
        :param server: The server to render.
        :param warn: Called for values Codex will send literally.
        :return: TOML text, without a trailing newline.
        """
        table = f"mcp_servers.{self._key(name)}"
        if isinstance(server, RemoteServer):
            lines, subtables = self._remote(name, server, warn)
        else:
            lines, subtables = self._stdio(name, server, warn)
        out = [f"[{table}]", *lines]
        for suffix, values in subtables.items():
            if values:
                out += ["", f"[{table}.{suffix}]"]
                out += [
                    f"{self._key(k)} = {self._string(v)}" for k, v in values.items()
                ]
        return "\n".join(out)

    def _remote(
        self, name: str, server: RemoteServer, warn: Warn
    ) -> tuple[list[str], dict[str, dict[str, str]]]:
        lines = [f"url = {self._string(server.url)}"]
        static: dict[str, str] = {}
        from_env: dict[str, str] = {}
        for header, value in server.headers.items():
            bearer = BEARER_ENV.fullmatch(value)
            whole = ENV_REF_PATTERN.fullmatch(value)
            if header.lower() == AUTHORIZATION and bearer:
                lines.append(f"bearer_token_env_var = {self._string(bearer.group(1))}")
            elif whole:
                from_env[header] = whole.group(1)
            else:
                if ENV_REF_PATTERN.search(value):
                    warn(
                        f"{name}: header {header} mixes text and ${{env:...}}; "
                        "Codex sends it as is"
                    )
                static[header] = value
        return lines, {"http_headers": static, "env_http_headers": from_env}

    def _stdio(
        self, name: str, server: StdioServer, warn: Warn
    ) -> tuple[list[str], dict[str, dict[str, str]]]:
        if any(ENV_REF_PATTERN.search(arg) for arg in server.args):
            warn(f"{name}: Codex does not expand ${{env:...}} in args")
        lines = [
            f"command = {self._string(server.command)}",
            f"args = {self._array(server.args)}",
        ]
        passthrough = [
            key for key, value in server.env.items() if value == f"${{env:{key}}}"
        ]
        literal = {
            key: value for key, value in server.env.items() if key not in passthrough
        }
        if passthrough:
            lines.append(f"env_vars = {self._array(passthrough)}")
        return lines, {"env": literal}

    @staticmethod
    def _string(value: str) -> str:
        return json.dumps(
            value, ensure_ascii=False
        )  # JSON strings are valid TOML basic strings

    def _key(self, key: str) -> str:
        return key if BARE_KEY.fullmatch(key) else self._string(key)

    def _array(self, values: tuple[str, ...] | list[str]) -> str:
        return "[" + ", ".join(self._string(value) for value in values) + "]"
