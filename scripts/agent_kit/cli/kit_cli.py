"""The ``kit.py`` command line and the composition root that wires the services."""

import argparse
import logging
from collections.abc import Callable, Sequence
from pathlib import Path

from agent_kit.clients import ClientRegistry
from agent_kit.console_reporter import ConsoleReporter
from agent_kit.errors import AppError
from agent_kit.files import TargetWriter
from agent_kit.library import Library, LibraryValidator
from agent_kit.models import InstallPlan, InstallRequest, KitLayout
from agent_kit.reporter_protocol import ReporterProtocol
from agent_kit.services import Installer, InstallPlanner
from agent_kit.utils import split_csv

logger = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_ERROR = 1

type Command = Callable[[argparse.Namespace], int]
type SubParsers = argparse._SubParsersAction[argparse.ArgumentParser]


class KitCli:
    """Parses arguments, wires the services, runs one command, reports the result."""

    def __init__(
        self, layout: KitLayout, reporter: ReporterProtocol | None = None
    ) -> None:
        self._layout = layout
        self._reporter = reporter or ConsoleReporter()
        self._registry = ClientRegistry()

    def run(self, argv: Sequence[str] | None = None) -> int:
        """Run one command.

        :param argv: Arguments without the program name; ``None`` reads ``sys.argv``.
        :return: The process exit code.
        """
        args = self.build_parser().parse_args(argv)
        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
        command: Command = args.command_handler
        try:
            return command(args)
        except AppError as exc:
            logger.debug("command %s failed", args.command, exc_info=True)
            self._reporter.error(str(exc))
            return EXIT_ERROR

    def build_parser(self) -> argparse.ArgumentParser:
        """Describe every command and option.

        :return: The configured parser.
        """
        parser = argparse.ArgumentParser(
            prog="kit.py", description="Install agent-kit profiles."
        )
        parser.add_argument(
            "--verbose", action="store_true", help="log debug details to stderr"
        )
        commands = parser.add_subparsers(
            dest="command", required=True, metavar="COMMAND"
        )
        self._add_list(commands)
        self._add_detect(commands)
        self._add_install(commands)
        self._add_check(commands)
        return parser

    # --- command definitions ------------------------------------------------------

    def _add_list(self, commands: SubParsers) -> None:
        parser = commands.add_parser("list", help="list available profiles")
        parser.set_defaults(command_handler=self._list)

    def _add_detect(self, commands: SubParsers) -> None:
        parser = commands.add_parser(
            "detect", help="show which clients a target already uses"
        )
        parser.add_argument("--target", required=True, help="project directory")
        parser.set_defaults(command_handler=self._detect)

    def _add_install(self, commands: SubParsers) -> None:
        parser = commands.add_parser("install", help="install profiles into a target")
        parser.add_argument("--target", required=True, help="project directory")
        parser.add_argument(
            "--client",
            default="",
            help=f"comma-separated: {', '.join(self._registry.names())}",
        )
        parser.add_argument(
            "--profile", action="append", default=[], help="comma-separated profiles"
        )
        parser.add_argument(
            "--no-core", action="store_true", help="do not add the core profile"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="overwrite existing rules, templates, MCP",
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="print the changes, write nothing"
        )
        parser.set_defaults(command_handler=self._install)

    def _add_check(self, commands: SubParsers) -> None:
        parser = commands.add_parser("check", help="validate the library")
        parser.set_defaults(command_handler=self._check)

    # --- command handlers ---------------------------------------------------------

    def _library(self) -> Library:
        return Library.discover(self._layout)

    def _list(self, args: argparse.Namespace) -> int:
        for name in self._library().profile_names():
            self._reporter.info(name)
        return EXIT_OK

    def _detect(self, args: argparse.Namespace) -> int:
        found = self._registry.detect(Path(args.target))
        for client, markers in found.items():
            self._reporter.info(f"{client:<9} {', '.join(markers)}")
        if len(found) == 1:
            self._reporter.info(f"detected: {next(iter(found))}")
        else:
            summary = f"several ({', '.join(found)})" if found else "none"
            self._reporter.info(f"detected: {summary}")
        return EXIT_OK

    def _install(self, args: argparse.Namespace) -> int:
        library = self._library()
        request = InstallRequest(
            target=Path(args.target),
            clients=tuple(split_csv([args.client])),
            profiles=tuple(split_csv(args.profile)),
            include_core=not args.no_core,
            force=args.force,
            dry_run=args.dry_run,
        )
        plan = InstallPlanner(library, self._registry).plan(request)
        self._print_plan(plan)
        writer = TargetWriter(
            plan.target, self._reporter, force=args.force, dry_run=args.dry_run
        )
        installer = Installer(self._layout, self._registry, self._reporter)
        for warning in installer.install(plan, writer):
            self._reporter.warn(warning)
        if args.dry_run:
            self._reporter.info("\nDry run. No files written.")
        return EXIT_OK

    def _print_plan(self, plan: InstallPlan) -> None:
        self._reporter.info(f"Profiles: {', '.join(plan.selection.profiles)}")
        self._reporter.info(
            f"Clients:  {', '.join(plan.clients)} ({plan.client_source})"
        )
        self._reporter.info(f"Target:   {plan.target}")
        for library in plan.libraries:
            self._reporter.info(f"Library:  {library}")
        self._reporter.info("")

    def _check(self, args: argparse.Namespace) -> int:
        problems = LibraryValidator().problems(self._library())
        for problem in problems:
            self._reporter.error(problem)
        if not problems:
            self._reporter.info("Library OK.")
        return EXIT_ERROR if problems else EXIT_OK
