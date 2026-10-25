"""Tests for agent_kit.utils."""

import pytest

from agent_kit import utils
from agent_kit.utils import JsonValue


def test_unique_keeps_first_order_and_drops_empty() -> None:
    assert utils.unique(["b", "a", "", "b", "c"]) == ["b", "a", "c"]


def test_split_csv_splits_and_trims() -> None:
    assert utils.split_csv(["a, b", "", " c "]) == ["a", "b", "c"]


def test_rewrite_env_refs_walks_nested_values() -> None:
    value: JsonValue = {"h": ["Bearer ${env:TOKEN}", 3], "plain": "x"}
    assert utils.rewrite_env_refs(value, r"${\1}") == {
        "h": ["Bearer ${TOKEN}", 3],
        "plain": "x",
    }


def test_retry_succeeds_after_transient_lock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agent_kit.utils.time.sleep", lambda _: None)
    calls: list[int] = []

    def flaky() -> None:
        calls.append(1)
        if len(calls) < 3:
            raise PermissionError("locked")

    utils.retry_on_permission_error(flaky)
    assert len(calls) == 3


def test_retry_gives_up_after_last_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agent_kit.utils.time.sleep", lambda _: None)

    def locked() -> None:
        raise PermissionError("locked")

    with pytest.raises(PermissionError):
        utils.retry_on_permission_error(locked)
