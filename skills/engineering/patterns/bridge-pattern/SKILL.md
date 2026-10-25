---
name: bridge-pattern
description: >-
  Generic Bridge pattern: decouple an abstraction from its implementation so
  both can vary independently, avoiding an N×M inheritance explosion. Use
  when two dimensions of variation multiply (shape × renderer, device × OS,
  notification type × channel), in any language or project.
---

# Bridge Pattern (Portable Template)

## When to Use

Activate when:
- Two independent dimensions of variation exist and inheritance would force one class per combination (`SvgCircle`, `RasterCircle`, `SvgSquare`, `RasterSquare`, ...)
- You expect to add new variants on *either* dimension over time and don't want that to multiply the class count
- The two dimensions genuinely vary independently — a shape doesn't care which renderer draws it, and a renderer doesn't care which shape it's drawing

Do **not** use when:
- Only one dimension actually varies — plain inheritance or Strategy already covers it with less indirection
- The two "dimensions" are actually coupled (one determines the other) — the independence Bridge assumes doesn't hold, so it just adds ceremony

## Template

```python
from typing import Protocol

class Renderer(Protocol):
    def render_circle(self, radius: float) -> str: ...

class SvgRenderer:
    def render_circle(self, radius: float) -> str:
        return f"<circle r='{radius}'/>"

class RasterRenderer:
    def render_circle(self, radius: float) -> str:
        return f"raster pixels for r={radius}"

class Shape:
    def __init__(self, renderer: Renderer) -> None:
        self._renderer = renderer

class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float) -> None:
        super().__init__(renderer)
        self._radius = radius

    def draw(self) -> str:
        return self._renderer.render_circle(self._radius)
```

`Shape` subclasses (Circle, Square, ...) and `Renderer` implementations (Svg, Raster, ...) vary independently — `N` shapes × `M` renderers stays `N + M` classes, composed at construction time, instead of `N * M` classes.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Abstraction hierarchy | `Shape`, `Circle`, `Square` — the "what" |
| Implementation hierarchy | `Renderer`, `SvgRenderer`, `RasterRenderer` — the "how" |
| Bridge | The abstraction holds a reference to the implementation interface, injected at construction |

## Anti-Patterns

- Introducing Bridge for a single dimension "in case a second one shows up later" — wait for the second dimension to actually exist
- Letting the abstraction reach into implementation-specific details instead of going through the `Renderer` interface, which quietly re-couples the two hierarchies
- Confusing this with Abstract Factory — Bridge is about runtime composition of two independent hierarchies, not about producing a consistent family of objects

## Related Skills

- `design-patterns-catalog` — choosing Bridge vs. Abstract Factory vs. Strategy
- `abstract-factory-pattern` — related decoupling shape, for a fixed family rather than two independently-varying dimensions
- `strategy-pattern` — Bridge is sometimes described as "Strategy applied to structure" — same injected-interface mechanic, different intent (structural decoupling vs. swappable algorithm)
