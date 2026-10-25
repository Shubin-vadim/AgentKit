---
name: proxy-pattern
description: >-
  Generic Proxy pattern: a stand-in that controls access to a real object —
  lazy loading, access checks, remote calls, or caching — behind the same
  interface as the real thing. Use when you need to intercept access without
  changing the real object's interface, in any language or project.
---

# Proxy Pattern (Portable Template)

## When to Use

Activate when:
- Construction or access to the real object is expensive and should be deferred until actually needed (lazy loading)
- You need to add an access check, rate limit, or permission gate in front of an object without changing its interface
- You're wrapping a remote resource (RPC, HTTP) behind a local-looking interface
- You want to cache results of the real object's calls transparently to callers

Do **not** use when:
- There's nothing to intercept — the real object can just be used directly, and the proxy is pure indirection with no job to do
- You actually need to *add new behavior* on top of the result (transform, combine) rather than *control access* to the call — that's Decorator

## Template

```python
from typing import Protocol

class Image(Protocol):
    def render(self) -> None: ...

class ExpensiveImage:
    def __init__(self, path: str) -> None:
        self._path = path
        self._load()  # expensive I/O

    def _load(self) -> None: ...
    def render(self) -> None: ...

class LazyImageProxy:
    def __init__(self, path: str) -> None:
        self._path = path
        self._real: ExpensiveImage | None = None

    def render(self) -> None:
        if self._real is None:
            self._real = ExpensiveImage(self._path)  # loaded on first use only
        self._real.render()
```

`LazyImageProxy` implements the exact same interface (`Image`/`render()`), so callers can't tell whether they're holding the real object or the proxy — until the first real call, nothing expensive has happened.

## Common Proxy Variants

| Variant | Purpose |
|---|---|
| **Virtual proxy** | Defer expensive construction until first use (example above) |
| **Protection proxy** | Check permissions before delegating to the real object |
| **Remote proxy** | Make a network call look like a local method call |
| **Caching proxy** | Memoize the real object's results, invalidate on a policy |

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Proxy class | `XxxProxy`, or `Lazy...`/`Cached...`/`Remote...` prefix naming the variant |
| Wrapped instance | `self._real` / `self._target`, created lazily or injected |

## Anti-Patterns

- A proxy that changes the interface of the real object — breaks transparent substitution, which is the entire point
- Caching proxies with no invalidation strategy, silently serving stale data forever
- Layering a proxy in front of something already cheap and local "for consistency" — adds a call frame and a file to read for zero benefit

## Related Skills

- `design-patterns-catalog` — choosing Proxy vs. Decorator vs. Adapter
- `decorator-pattern` — same wrapper shape, but for adding behavior rather than controlling access
