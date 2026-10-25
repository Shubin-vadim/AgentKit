---
name: mediator-pattern
description: >-
  Generic Mediator pattern: centralize how a set of objects interact instead
  of them referencing each other directly. Use when many objects have
  tangled peer-to-peer references (form field cross-validation, chat rooms,
  UI widget coordination), in any language or project.
---

# Mediator Pattern (Portable Template)

## When to Use

Activate when:
- Several objects reference each other directly and adding a new one means updating every existing peer
- You're coordinating UI widgets, chat participants, or workflow steps where interactions are many-to-many, not a fixed pipeline
- You want to unit-test one participant's behavior without instantiating every other participant it currently talks to directly

Do **not** use when:
- Only two objects interact — a direct reference is simpler and the mediator adds a layer with nothing to centralize
- The interactions are actually a fixed, ordered sequence — Chain of Responsibility or a plain pipeline function models that more directly than a hub-and-spoke mediator

## Template

```python
class DialogMediator:
    def __init__(self, checkbox: "Checkbox", submit_button: "SubmitButton") -> None:
        self._checkbox = checkbox
        self._submit_button = submit_button

    def notify(self, sender: str, event: str) -> None:
        if sender == "checkbox" and event == "toggled":
            self._submit_button.set_enabled(self._checkbox.is_checked)

class Checkbox:
    def __init__(self, mediator: DialogMediator) -> None:
        self._mediator = mediator
        self.is_checked = False

    def toggle(self) -> None:
        self.is_checked = not self.is_checked
        self._mediator.notify("checkbox", "toggled")
```

Widgets call `self._mediator.notify(...)` instead of reaching for other widgets directly — adding a third widget means teaching the mediator one new rule, not touching every existing widget.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Mediator | `XxxMediator`, or named for the coordinated whole (`DialogController`, `ChatRoom`) |
| Participants | Hold a reference to the mediator, call `notify`/`send` rather than each other |

## Anti-Patterns

- A mediator that grows into a god-object containing all the actual business logic instead of just coordination — push real logic back into the participants or a service
- Participants that still hold direct references to each other "just in case," alongside the mediator reference — pick one communication path
- Introducing a mediator for two objects that will only ever be two objects

## Related Skills

- `design-patterns-catalog` — choosing Mediator vs. Observer vs. Chain of Responsibility
- `observer-pattern` — one-to-many broadcast; Mediator is the many-to-many, bidirectional cousin
- `facade-pattern` — both centralize access to multiple objects, but Facade simplifies an external-facing API while Mediator coordinates peers that already know about each other
