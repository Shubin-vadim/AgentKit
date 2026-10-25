---
name: memento-pattern
description: >-
  Generic Memento pattern: capture and restore an object's internal state
  without violating its encapsulation. Use for undo/rollback/snapshot
  features, in any language or project.
---

# Memento Pattern (Portable Template)

## When to Use

Activate when:
- You need undo, rollback, or point-in-time snapshots of a mutable object's internal state
- The object's internals shouldn't be exposed to whoever is storing/managing the history (an undo stack, a version list)
- Snapshots need to be opaque tokens passed around by callers that never read or mutate their contents directly

Do **not** use when:
- Values are already plain and immutable — just keep a list of past values directly, no wrapper type needed
- Full state snapshots are prohibitively large for how often they're taken — consider capturing diffs/commands instead (see `command-pattern`) rather than whole-state mementos

## Template

```python
class EditorMemento:
    def __init__(self, content: str) -> None:
        self._content = content  # private to the originator; treat as opaque outside Editor

class Editor:
    def __init__(self) -> None:
        self.content = ""

    def save(self) -> EditorMemento:
        return EditorMemento(self.content)

    def restore(self, memento: EditorMemento) -> None:
        self.content = memento._content

editor = Editor()
editor.content = "draft v1"
checkpoint = editor.save()
editor.content = "draft v2 - broke something"
editor.restore(checkpoint)  # back to "draft v1"
```

`EditorMemento` is created and read only by `Editor` itself — the caretaker (whatever holds `checkpoint`) just stores and passes it back, never reaching into it.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Originator | The object whose state is being captured (`Editor`) |
| Memento | `XxxMemento`, an otherwise-opaque snapshot type |
| Caretaker | Whatever stores mementos (an undo stack, a history list) — never inspects their contents |

## Anti-Patterns

- A caretaker that reaches into the memento's internals instead of treating it as opaque — breaks the encapsulation this pattern exists to preserve
- Snapshotting the entire object graph when only a small, cheap-to-copy subset actually needs to be restorable
- Using Memento for values that are already immutable — that's just keeping a list, no pattern needed

## Related Skills

- `design-patterns-catalog` — choosing Memento vs. Command for undo (Memento captures state; Command captures the reversible action)
- `command-pattern` — often paired with Memento: command executes the change, memento captures the "before" to restore on undo
- `prototype-pattern` — related "clone to preserve a copy" idea, but Prototype is for making new independent objects, not for restoring a past state of the same object
