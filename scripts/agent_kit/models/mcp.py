"""MCP server models: a local stdio launch or a remote HTTP endpoint.

Secrets are written as ``${env:NAME}``; each client adapter rewrites them.
"""

from pydantic import BaseModel, ConfigDict, Field


class StdioServer(BaseModel):
    """An MCP server the client starts as a local process."""

    model_config = ConfigDict(frozen=True)

    command: str
    args: tuple[str, ...] = ()
    env: dict[str, str] = Field(default_factory=dict)


class RemoteServer(BaseModel):
    """An MCP server the client reaches over HTTP."""

    model_config = ConfigDict(frozen=True)

    url: str
    headers: dict[str, str] = Field(default_factory=dict)


type McpServer = StdioServer | RemoteServer
