"""Tests for agent_kit.console_reporter."""

import io

from agent_kit.console_reporter import ConsoleReporter


def make() -> tuple[ConsoleReporter, io.StringIO, io.StringIO]:
    out, err = io.StringIO(), io.StringIO()
    return ConsoleReporter(out, err), out, err


def test_action_aligns_verb_and_adds_note() -> None:
    reporter, out, _ = make()
    reporter.action("mcp", ".mcp.json", "github")
    assert out.getvalue() == "mcp       .mcp.json [github]\n"


def test_info_goes_to_stdout() -> None:
    reporter, out, err = make()
    reporter.info("hello")
    assert (out.getvalue(), err.getvalue()) == ("hello\n", "")


def test_warn_goes_to_stderr() -> None:
    reporter, _, err = make()
    reporter.warn("careful")
    assert err.getvalue() == "warning: careful\n"


def test_error_goes_to_stderr() -> None:
    reporter, _, err = make()
    reporter.error("broken")
    assert err.getvalue() == "error: broken\n"
