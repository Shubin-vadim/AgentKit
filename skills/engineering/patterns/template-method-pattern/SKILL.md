---
name: template-method-pattern
description: >-
  Generic Template Method pattern: a fixed algorithm skeleton lives in a base
  class, subclasses override only the steps that differ. Use when several
  classes share the same overall steps but differ in a few, in any language
  or project.
---

# Template Method Pattern (Portable Template)

## When to Use

Activate when:
- Several classes already implement the same sequence of steps, with only a subset of steps actually varying between them
- You want to guarantee the overall order of steps can't be gotten wrong by subclass authors
- A shared setup/teardown wraps a variable middle step (parse-then-store, with parsing varying by format)

Do **not** use when:
- Subclasses end up overriding most of the steps anyway — the shared skeleton isn't buying anything, and composition (Strategy, plain functions) will be more flexible
- There's only one implementation and no second one planned — there's no "template" to extract yet

## Template

```python
from abc import ABC, abstractmethod

class DataImporter(ABC):
    def run(self, path: str) -> None:
        raw = self._read(path)
        parsed = self._parse(raw)
        self._store(parsed)

    def _read(self, path: str) -> bytes:
        return open(path, "rb").read()

    @abstractmethod
    def _parse(self, raw: bytes) -> list[dict]: ...

    def _store(self, rows: list[dict]) -> None:
        Database.bulk_insert(rows)

class CsvImporter(DataImporter):
    def _parse(self, raw: bytes) -> list[dict]:
        return parse_csv(raw)

class JsonImporter(DataImporter):
    def _parse(self, raw: bytes) -> list[dict]:
        return parse_json(raw)
```

`run()` is fixed and never overridden; `CsvImporter`/`JsonImporter` only supply the one step that actually differs.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Base class | Named for the overall process (`DataImporter`) |
| Template method | The fixed-order method (`run`), typically not overridden, sometimes `final` where the language supports it |
| Hook methods | Prefixed to signal override intent (`_parse` abstract = must override; `_read`/`_store` concrete = may override) |

## Anti-Patterns

- A "template method" where every subclass overrides every step — there's no shared algorithm left to protect, just an interface; consider Strategy instead
- Hook methods with side effects subclasses don't expect, making override order-sensitive in surprising ways
- Deep template-method hierarchies (subclass of a subclass of a subclass) — favor composition over multiple inheritance layers once it gets past one level

## Related Skills

- `design-patterns-catalog` — choosing Template Method vs. Strategy (inheritance-based fixed skeleton vs. composition-based swappable algorithm)
- `strategy-pattern` — the composition-based alternative when the "steps" should be swappable independently of a class hierarchy
