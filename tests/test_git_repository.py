"""Tests for agent_kit.git_repository."""

from pathlib import Path

from utils import git, write

from agent_kit.git_repository import UNKNOWN, GitRepository


def make_repo(path: Path) -> GitRepository:
    git(path.parent, "init", "-q", str(path))
    git(path, "config", "user.email", "t@example.test")
    git(path, "config", "user.name", "Test")
    return GitRepository(path)


def test_revision_unknown_without_commits_then_sha(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r")
    assert repo.revision() == UNKNOWN
    write(tmp_path / "r" / "a.txt", "a")
    git(tmp_path / "r", "add", ".")
    git(tmp_path / "r", "commit", "-q", "-m", "init")
    assert len(repo.revision()) == 40


def test_dirty_reports_changes(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r")
    assert repo.dirty() == "false"
    write(tmp_path / "r" / "new.txt", "n")
    assert repo.dirty() == "true"


def test_files_lists_untracked_and_respects_gitignore(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "r")
    write(tmp_path / "r" / ".gitignore", "*.log\n")
    write(tmp_path / "r" / "a.md", "a")
    write(tmp_path / "r" / "x.log", "x")
    assert repo.files() == [".gitignore", "a.md"]


def test_everything_degrades_outside_git(tmp_path: Path) -> None:
    repo = GitRepository(tmp_path / "missing")
    assert (repo.revision(), repo.dirty(), repo.files()) == (UNKNOWN, UNKNOWN, None)
