---
name: abstract-factory-pattern
description: >-
  Generic Abstract Factory pattern: produce a family of related objects
  together so they stay consistent with each other. Use when you must swap
  an entire family of implementations (UI theme, database driver family,
  cloud provider SDKs) as one unit, in any language or project. Pair with
  design-patterns-catalog for picking Abstract Factory vs. plain Factory
  Method.
---

# Abstract Factory Pattern (Portable Template)

## When to Use

Activate when:
- Multiple related product types must be created together and stay mutually consistent (a UI theme's button *and* checkbox *and* dialog must all match)
- You expect to swap the whole family at a single composition-root decision point (dev vs. prod drivers, light vs. dark theme, AWS vs. GCP clients)
- Mixing products from different families would be a bug you want the type system to prevent

Do **not** use when:
- Only one product type ever varies — that's plain Factory Method, this adds a layer of indirection with no payoff
- The "families" don't actually need to be consistent with each other — you'd be inventing structure that isn't there

## Template

```python
from typing import Protocol

class Button(Protocol):
    def render(self) -> str: ...

class Checkbox(Protocol):
    def render(self) -> str: ...

class WidgetFactory(Protocol):
    def create_button(self) -> Button: ...
    def create_checkbox(self) -> Checkbox: ...

class DarkWidgetFactory:
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()

class LightWidgetFactory:
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()

def render_dialog(factory: WidgetFactory) -> None:
    factory.create_button().render()
    factory.create_checkbox().render()
```

`render_dialog` never checks which theme is active — pass the right `WidgetFactory` once, at the composition root, and every widget it produces matches.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Abstract factory | `WidgetFactory`, `ClientFactory` — named for the family's purpose |
| Concrete factories | `DarkWidgetFactory`, `LightWidgetFactory` — named for the variant of the family |
| Product interfaces | `Button`, `Checkbox` — named for the role, one per product type in the family |

## Anti-Patterns

- Passing the concrete factory (`DarkWidgetFactory`) instead of the `WidgetFactory` interface into consuming code — reintroduces the coupling this pattern exists to remove
- A factory whose products don't actually need to be consistent with each other — split into independent Factory Methods instead
- Growing the factory interface every time one new product type shows up in only one family variant — that product probably doesn't belong in the shared abstract interface

## Related Skills

- `design-patterns-catalog` — choosing Abstract Factory vs. Factory Method vs. Builder
- `factory-method-pattern` — the single-product version of this idea
- `bridge-pattern` — related "decouple abstraction from implementation" shape, for when you need the two dimensions to vary independently rather than as a fixed family
