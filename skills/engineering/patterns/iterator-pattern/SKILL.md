---
name: iterator-pattern
description: >-
  Generic Iterator pattern: sequential access to a collection's elements
  without exposing its underlying structure. Use when writing custom
  traversal over a custom collection, in any language or project — most
  modern languages already give you this via a built-in iteration protocol.
---

# Iterator Pattern (Portable Template)

## When to Use

Activate when:
- You've built a custom collection or tree and want callers to traverse it with the language's standard `for`/`foreach` syntax
- Traversal order/logic (skip every Nth element, depth-first over a tree, lazy/streamed reads) is non-trivial enough to deserve encapsulating once, in one place

Do **not** use when:
- The language's built-in iteration protocol already covers the case — implement that protocol (`__iter__`/`Iterable` in Python, `Iterator`/`Iterable` in Java, `Symbol.iterator` in JS) rather than hand-rolling a bespoke `hasNext()/next()` interface; that hand-rolled interface is exactly what the GoF pattern predates and the language has since absorbed
- A plain list/array with standard indexing already serves every caller's need

## Template

```python
from typing import Iterator

class SkipList:
    def __init__(self, items: list[int], step: int) -> None:
        self._items, self._step = items, step

    def __iter__(self) -> Iterator[int]:
        return iter(self._items[:: self._step])

for value in SkipList([1, 2, 3, 4, 5, 6], step=2):
    print(value)  # 1, 3, 5
```

Implementing `__iter__` means `SkipList` works with `for`, `list(...)`, unpacking, and every other language construct that expects an iterable — for free.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Iterable | The collection class, implementing the language's iteration protocol |
| Iterator (if separate from the collection) | A small object holding traversal position, returned by the collection's `__iter__`/equivalent |

## Anti-Patterns

- Hand-rolling `has_next()`/`next()` methods in a language that already has a native iteration protocol — extra API surface for something the language does natively
- An iterator that mutates the underlying collection while iterating, causing skipped or duplicated elements
- Exposing the collection's internal storage directly ("just index into `self._items`") instead of going through iteration, coupling every caller to the internal representation

## Related Skills

- `design-patterns-catalog` — choosing Iterator vs. exposing a raw collection
- `composite-pattern` — frequently paired with Iterator to traverse a tree without exposing its recursive structure
