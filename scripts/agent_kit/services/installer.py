"""Carry out an install plan through the client adapters."""

import logging
import stat

from agent_kit.clients import AGENTS_MD, ClientAdapter, ClientRegistry
from agent_kit.files import FolderSync, TargetWriter
from agent_kit.models import InstallPlan, KitLayout, LockContents
from agent_kit.reporter_protocol import ReporterProtocol
from agent_kit.services.lock_writer import LockWriter

logger = logging.getLogger(__name__)

SHELL_SUFFIX = ".sh"


class Installer:
    """Writes a planned installation: skills, templates, rules, MCP, and lock."""

    def __init__(
        self,
        layout: KitLayout,
        registry: ClientRegistry,
        reporter: ReporterProtocol,
        folder_sync: FolderSync | None = None,
    ) -> None:
        self._layout = layout
        self._registry = registry
        self._reporter = reporter
        self._folder_sync = folder_sync or FolderSync()
        self._lock_writer = LockWriter()

    def install(self, plan: InstallPlan, writer: TargetWriter) -> list[str]:
        """Install everything the plan lists.

        :param plan: A plan from :class:`InstallPlanner`.
        :param writer: Writer bound to ``plan.target``.
        :return: Warnings the user should act on.
        :raises ConfigFileError: If a client's config file cannot be updated.
        :raises PermissionError: If a skill file stays locked after every retry.
        """
        adapters = [self._registry.get(name) for name in plan.clients]
        self._install_skills(plan, adapters, writer)
        self._install_templates(plan, writer)
        installs_agents_md = any(t.dest == AGENTS_MD for t in plan.templates)
        for adapter in adapters:
            if plan.rules:
                adapter.install_rules(writer, list(plan.rules))
            adapter.finish(writer, installs_agents_md)
            if plan.servers:
                adapter.install_mcp(writer, plan.servers)
        self._lock_writer.write(writer, self._lock_contents(plan))
        for adapter in adapters:
            for note in adapter.notes(plan.servers):
                self._reporter.info(f"note: {note}")
        return writer.warnings

    def _install_skills(
        self, plan: InstallPlan, adapters: list[ClientAdapter], writer: TargetWriter
    ) -> None:
        for src in plan.skills:
            for adapter in adapters:
                dest = plan.target / adapter.skills_dir / src.name
                writer.report("skill", dest)
                if not writer.dry_run:
                    self._folder_sync.sync(src, dest)

    @staticmethod
    def _install_templates(plan: InstallPlan, writer: TargetWriter) -> None:
        for template in plan.templates:
            dest = plan.target / template.dest
            writer.write_unless_present(dest, template.src.read_text(encoding="utf-8"))
            if not writer.dry_run and dest.suffix == SHELL_SUFFIX:
                dest.chmod(
                    dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                )

    def _lock_contents(self, plan: InstallPlan) -> LockContents:
        return LockContents(
            kit_root=self._layout.root,
            libraries=plan.libraries,
            clients=plan.clients,
            profiles=plan.selection.profiles,
            skills=plan.selection.skills,
            rules=plan.selection.rules,
            mcp=tuple(plan.servers),
            templates=tuple(t.dest for t in plan.templates),
        )
