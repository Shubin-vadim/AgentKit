---
name: command-pattern
description: >-
  Generic Command pattern: encapsulate a request as an object so it can be
  executed, queued, logged, or undone. Use when you need undo/redo, deferred
  execution, retry, or to pass "an action" around as a first-class value, in
  any language or project.
---

# Command Pattern (Portable Template)

## When to Use

Activate when:
- You need undo/redo history for user actions
- Actions must be queued, scheduled, retried, or logged before/after execution rather than run immediately inline
- You want to parameterize a caller with "an action to run later" rather than have it call a fixed method

Do **not** use when:
- A direct method call already expresses the intent and nothing needs to be deferred, queued, or undone — wrapping it in a command object is pure ceremony

## Template

```python
from typing import Protocol

class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...

class InsertTextCommand:
    def __init__(self, document: Document, text: str, position: int) -> None:
        self._document, self._text, self._position = document, text, position

    def execute(self) -> None:
        self._document.insert(self._position, self._text)

    def undo(self) -> None:
        self._document.delete(self._position, len(self._text))

class CommandHistory:
    def __init__(self) -> None:
        self._history: list[Command] = []

    def run(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if self._history:
            self._history.pop().undo()
```

Wrapping the action as an object is what makes undo, queueing, and retry possible — `CommandHistory` never needs to know what kind of action it's replaying.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Command interface | `Command` (`execute()`, and `undo()` if reversible) |
| Concrete commands | `XxxCommand`, named for the action (`InsertTextCommand`, `DeleteRowCommand`) |
| Invoker | Holds the history/queue, calls `execute()`/`undo()` without knowing command internals |

## Anti-Patterns

- Commands that reach back into global state instead of taking everything they need as constructor arguments — breaks replay/undo correctness
- An `undo()` that doesn't actually reverse `execute()`'s effect (partial rollback) — worse than no undo, because it corrupts state silently
- Wrapping every function call as a Command "for consistency" when nothing ever queues, logs, or undoes it

## Related Skills

- `design-patterns-catalog` — choosing Command vs. Strategy (Command is about *when/whether* to run an action; Strategy is about *which algorithm* computes a result)
- `memento-pattern` — often paired with Command for undo: memento captures state, command captures the action that changed it
