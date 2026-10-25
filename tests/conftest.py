"""Shared fixtures: a tiny kit on disk, an empty target, a reporter, a writer."""

from pathlib import Path

import pytest
from recording_reporter import RecordingReporter
from utils import build_kit

from agent_kit.files import TargetWriter
from agent_kit.library import Library
from agent_kit.models import KitLayout


@pytest.fixture
def kit(tmp_path: Path) -> KitLayout:
    """Build a minimal kit.

    :param tmp_path: Pytest's temporary folder.
    :return: The kit layout.
    """
    return KitLayout(root=build_kit(tmp_path / "kit"))


@pytest.fixture
def library(kit: KitLayout) -> Library:
    """Provide the minimal kit as a library.

    :param kit: The kit layout.
    :return: A library over the kit only.
    """
    return Library.discover(kit)


@pytest.fixture
def target(tmp_path: Path) -> Path:
    """Create an empty project folder.

    :param tmp_path: Pytest's temporary folder.
    :return: The project folder.
    """
    path = tmp_path / "project"
    path.mkdir()
    return path


@pytest.fixture
def reporter() -> RecordingReporter:
    """Provide a reporter that records output.

    :return: A fresh recording reporter.
    """
    return RecordingReporter()


@pytest.fixture
def writer(target: Path, reporter: RecordingReporter) -> TargetWriter:
    """Provide a writer bound to the empty target.

    :param target: The project folder.
    :param reporter: The recording reporter.
    :return: A writer without ``--force`` or dry run.
    """
    return TargetWriter(target, reporter, force=False, dry_run=False)
