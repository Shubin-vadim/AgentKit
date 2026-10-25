---
name: observer-pattern
description: >-
  Generic Observer pattern: one-to-many notification where a subject changes
  and subscribed observers react, without the subject knowing who's
  listening. Use for decoupled event/pubsub, UI reacting to model changes, or
  cache invalidation listeners, in any language or project.
---

# Observer Pattern (Portable Template)

## When to Use

Activate when:
- Multiple, possibly changing, listeners need to react to something happening, and the subject shouldn't need to know who or how many
- You're building an event bus, pubsub channel, or UI-reacts-to-model wiring
- New listeners will be added over time without touching the subject's code

Do **not** use when:
- There's exactly one fixed caller who needs to know — just call it directly, subscription machinery adds nothing
- Observers need a guaranteed *order* or *return value* back from the subject — Observer is fire-and-forget by design; use Chain of Responsibility or a plain pipeline if order/short-circuiting matters

## Template

```python
from typing import Protocol

class Observer(Protocol):
    def on_change(self, value: int) -> None: ...

class Counter:
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._value = 0

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def increment(self) -> None:
        self._value += 1
        for observer in self._observers:
            observer.on_change(self._value)

class LoggingObserver:
    def on_change(self, value: int) -> None:
        print(f"counter is now {value}")
```

`Counter` never imports or knows about `LoggingObserver` — it only depends on the `Observer` protocol.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Subject | The class owning `subscribe`/`unsubscribe`/`notify` |
| Observer interface | `Observer`, or named for the event (`ChangeListener`) |
| Notify method | `on_<event>`, `notify_<event>`, or a single `handle(event)` for multi-event subjects |

## Anti-Patterns

- Forgetting `unsubscribe`, leaking observers that keep the subject (or vice versa) alive longer than intended — a common memory-leak source in long-lived UIs and services
- Observers that throw and crash the whole notification loop for every other observer — isolate failures per observer if one bad listener shouldn't break the rest
- Using Observer where a simple return value or a direct call chain would be clearer — don't reach for pubsub machinery to connect two things that will only ever be two things

## Related Skills

- `design-patterns-catalog` — choosing Observer vs. Mediator vs. Chain of Responsibility
- `mediator-pattern` — centralizes many-to-many interaction instead of Observer's one-to-many broadcast
