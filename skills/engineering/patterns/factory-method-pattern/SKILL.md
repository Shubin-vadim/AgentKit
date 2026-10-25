---
name: factory-method-pattern
description: >-
  Generic Factory Method pattern: a creation point decides which concrete
  class to instantiate, callers depend only on the abstract product. Use when
  a base class or function knows *that* an object is needed but not *which*
  concrete type, in any language or project. Pair with
  design-patterns-catalog for picking Factory Method vs. Abstract Factory vs.
  Builder.
---

# Factory Method Pattern (Portable Template)

## When to Use

Activate when:
- A method is choosing between concrete implementations with an `if`/`switch` on a type/kind string, and every caller would otherwise repeat that same branch
- New concrete types will be added over time (new channel, new file format, new provider) and you want that list to live in one place
- Callers should depend on an abstract product interface, never on the concrete classes directly (keeps call sites stable as types are added/removed)

Do **not** use when:
- Only one concrete type exists and there is no second one on the roadmap — just construct it directly
- The "concrete types" don't actually share a common interface — unify the interface first, or this pattern has nothing to attach to

## Template

```python
from typing import Literal, Protocol

class Notifier(Protocol):
    def send(self, message: str) -> None: ...

class EmailNotifier:
    def send(self, message: str) -> None:
        print(f"email: {message}")

class SmsNotifier:
    def send(self, message: str) -> None:
        print(f"sms: {message}")

class NotifierFactory:
    @staticmethod
    def create(channel: Literal["email", "sms"]) -> Notifier:
        if channel == "email":
            return EmailNotifier()
        if channel == "sms":
            return SmsNotifier()
        raise ValueError(f"unknown channel: {channel}")
```

Callers depend on `Notifier`, never on `EmailNotifier`/`SmsNotifier`. Adding a channel means adding one branch here, not touching every call site that sends a notification.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Abstract product | `Notifier`, `Notifier` interface/protocol named for the *role* |
| Concrete products | `EmailNotifier`, `SmsNotifier` — named for the variant |
| Creation point | `XxxFactory.create(...)` or a plain `create_xxx(kind)` function |

## Anti-Patterns

- Duplicating the `if channel == ...` dispatch at every call site instead of centralizing it in one factory
- A factory that returns a concrete type instead of the abstract product — defeats the point, callers end up depending on the concrete class anyway
- Growing the factory's `create()` to also configure/validate/log — keep it to construction only; push cross-cutting concerns to a decorator or the caller

## Related Skills

- `design-patterns-catalog` — choosing Factory Method vs. Abstract Factory vs. Builder
