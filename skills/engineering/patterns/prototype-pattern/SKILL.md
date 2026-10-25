---
name: prototype-pattern
description: >-
  Generic Prototype pattern: create new objects by cloning a prototypical
  instance instead of constructing from scratch. Use when construction is
  expensive or reflective and you need many independent, near-identical
  variants, in any language or project.
---

# Prototype Pattern (Portable Template)

## When to Use

Activate when:
- Building an object from scratch is expensive (parsed from disk, built via reflection/DI, computed) and you need several near-identical copies
- You want to capture a "template" configuration once and stamp out independent variations of it without re-running full construction each time
- Object graphs are deep enough that manual field-by-field copying would be error-prone

Do **not** use when:
- Objects are cheap to construct normally — cloning adds a `clone()`/copy contract for no real savings
- A shallow copy would silently share mutable nested state you didn't mean to share — either implement a real deep clone or don't use this pattern

## Template

```python
import copy

class DocumentTemplate:
    def __init__(self, sections: list[str]) -> None:
        self.sections = sections

    def clone(self) -> "DocumentTemplate":
        return copy.deepcopy(self)

base = DocumentTemplate(sections=["intro", "body", "footer"])
draft = base.clone()
draft.sections.append("appendix")  # base.sections is untouched — deep clone, no shared state
```

Prefer the language's built-in deep-copy facility (`copy.deepcopy` in Python, a copy constructor, a serialize/deserialize round-trip) over a hand-rolled field-by-field clone, which silently misses new fields as the class evolves.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Clone method | `clone()` (or the language's copy-constructor idiom) |
| Prototype registry (if used) | `PrototypeRegistry` holding named base instances to clone from |

## Anti-Patterns

- A hand-written `clone()` that copies fields individually and silently drifts out of sync as new fields are added — prefer the language's generic deep-copy mechanism
- Cloning when a shared immutable value would do just as well with no copying at all
- Shallow-cloning an object with mutable nested collections, then being surprised the "independent" copies share state

## Related Skills

- `design-patterns-catalog` — choosing Prototype vs. Factory Method vs. Builder
