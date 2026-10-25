---
name: state-pattern
description: >-
  Generic State pattern: an object changes behavior when its internal state
  changes, so it appears to change class. Use for explicit state machines
  with state-specific behavior — order lifecycle, connection states, workflow
  steps — in any language or project.
---

# State Pattern (Portable Template)

## When to Use

Activate when:
- An object has a small number of well-defined states, and behavior genuinely differs by state (not just a field value, but different logic per state)
- Methods are growing `if self.status == "x": ... elif self.status == "y": ...` blocks repeated across several methods
- Invalid transitions (e.g. shipping an already-delivered order) should be caught explicitly rather than silently allowed

Do **not** use when:
- A couple of boolean flags already model the behavior clearly and there's no real "current state object" worth extracting
- States don't actually have different *behavior*, only different *data* — a plain enum field is enough

## Template

```python
from typing import Protocol

class OrderState(Protocol):
    def next(self, order: "Order") -> None: ...

class Placed:
    def next(self, order: "Order") -> None:
        order.state = Shipped()

class Shipped:
    def next(self, order: "Order") -> None:
        order.state = Delivered()

class Delivered:
    def next(self, order: "Order") -> None:
        raise ValueError("already delivered")

class Order:
    def __init__(self) -> None:
        self.state: OrderState = Placed()

    def advance(self) -> None:
        self.state.next(self)
```

Each state class owns its own transition logic; `Order.advance()` never branches on "what state am I in" — it just delegates.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| State interface | `XxxState` (`OrderState`) |
| Concrete states | Named for the state itself (`Placed`, `Shipped`, `Delivered`), not `XxxStateImpl` |
| Context object | Holds `self.state: XxxState` and delegates behavior to it |

## Anti-Patterns

- The context still checking `isinstance(self.state, Shipped)` anywhere — defeats the point, put that logic inside the state class
- States that need to know about every other state to decide "can I transition to X" — usually a sign the transition rules should live in a small explicit state-machine table instead
- Using this for two states with no real behavioral difference — a boolean is simpler

## Related Skills

- `design-patterns-catalog` — choosing State vs. Strategy (State changes over an object's lifetime as a side effect of its own actions; Strategy is chosen once by the caller and doesn't self-transition)
- `strategy-pattern` — same "swap an interface implementation" shape, different intent
