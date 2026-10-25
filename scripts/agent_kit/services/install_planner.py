"""Resolve an install request into a complete, validated plan."""

import logging
from pathlib import Path

from agent_kit.clients import ClientRegistry
from agent_kit.errors import InstallError
from agent_kit.library import Library, McpFragmentLoader, RuleParser
from agent_kit.models import InstallPlan, InstallRequest, McpServer, TemplateFile

logger = logging.getLogger(__name__)


class InstallPlanner:
    """Checks the target and resolves every asset before anything is written."""

    def __init__(
        self,
        library: Library,
        registry: ClientRegistry,
        rule_parser: RuleParser | None = None,
        mcp_loader: McpFragmentLoader | None = None,
    ) -> None:
        self._library = library
        self._registry = registry
        self._rule_parser = rule_parser or RuleParser()
        self._mcp_loader = mcp_loader or McpFragmentLoader()

    def plan(self, request: InstallRequest) -> InstallPlan:
        """Validate the request and resolve every asset it needs.

        :param request: What the user asked for.
        :return: The plan the installer carries out.
        :raises InstallError: If the target is invalid or the client is unclear.
        :raises LibraryError: If a profile or asset is missing or duplicated.
        :raises ConfigFileError: If a client cannot handle the target's config files.
        """
        target = self._checked_target(request.target)
        clients, source = self._clients(target, list(request.clients))
        selection = self._library.select(list(request.profiles), request.include_core)
        servers: dict[str, McpServer] = {}
        for name in selection.mcp:
            servers.update(self._mcp_loader.load(self._library.mcp_fragment(name)))
        logger.debug("planned %s for %s", selection.profiles, clients)
        return InstallPlan(
            target=target,
            clients=tuple(clients),
            client_source=source,
            libraries=tuple(self._library.extra_roots),
            selection=selection,
            skills=tuple(self._library.skill(name) for name in selection.skills),
            rules=tuple(
                self._rule_parser.parse(self._library.rule(n)) for n in selection.rules
            ),
            servers=servers,
            templates=tuple(
                TemplateFile(src=self._library.template(spec.src), dest=spec.dest)
                for spec in selection.templates
            ),
        )

    def _checked_target(self, target: Path) -> Path:
        resolved = target.resolve()
        if not resolved.is_dir():
            raise InstallError(f"Target is not an existing directory: {target}")
        if self._library.contains(resolved):
            raise InstallError(
                f"Refusing to install into a kit library ({resolved}). "
                "Pass a project directory."
            )
        return resolved

    def _clients(self, target: Path, requested: list[str]) -> tuple[list[str], str]:
        source = "from --client"
        if not requested:
            found = self._registry.detect(target)
            if len(found) != 1:
                raise InstallError(
                    f"Cannot pick a client for {target} "
                    f"(found: {', '.join(found) or 'none'}). "
                    f"Ask the user which client they use, then pass "
                    f"--client {'|'.join(self._registry.names())}."
                )
            requested = list(found)
            source = "detected from " + ", ".join(next(iter(found.values())))
        for name in requested:
            self._registry.get(name).preflight(target)
        return requested, source
