"""Models for one installation: the request, the resolved plan, and the lock."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from agent_kit.models.library import Selection
from agent_kit.models.mcp import McpServer
from agent_kit.models.rule import Rule


class InstallRequest(BaseModel):
    """What the user asked for on the command line."""

    model_config = ConfigDict(frozen=True)

    target: Path
    clients: tuple[str, ...] = ()
    profiles: tuple[str, ...] = ()
    include_core: bool = True
    force: bool = False
    dry_run: bool = False


class TemplateFile(BaseModel):
    """One template source and where it lands in the target."""

    model_config = ConfigDict(frozen=True)

    src: Path
    dest: str


class InstallPlan(BaseModel):
    """Everything resolved and validated before the first write."""

    model_config = ConfigDict(frozen=True)

    target: Path
    clients: tuple[str, ...]
    client_source: str
    libraries: tuple[Path, ...]
    selection: Selection
    skills: tuple[Path, ...]
    rules: tuple[Rule, ...]
    servers: dict[str, McpServer]
    templates: tuple[TemplateFile, ...]


class LockContents(BaseModel):
    """What ``.agent-kit.lock`` records about one installation."""

    model_config = ConfigDict(frozen=True)

    kit_root: Path
    libraries: tuple[Path, ...]
    clients: tuple[str, ...]
    profiles: tuple[str, ...]
    skills: tuple[str, ...]
    rules: tuple[str, ...]
    mcp: tuple[str, ...]
    templates: tuple[str, ...]
