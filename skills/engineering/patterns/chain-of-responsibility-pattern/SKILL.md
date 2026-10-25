---
name: chain-of-responsibility-pattern
description: >-
  Generic Chain of Responsibility pattern: pass a request along a chain of
  handlers until one of them handles it. Use for middleware pipelines,
  validation chains, event bubbling, or fallback resolution, in any language
  or project.
---

# Chain of Responsibility Pattern (Portable Template)

## When to Use

Activate when:
- A request must pass through a sequence of independent checks/transforms, any of which might short-circuit the rest (auth, then rate-limit, then handler)
- The set and order of handlers needs to change without touching the handlers themselves — most middleware stacks are already this pattern
- You want each handler to know nothing about the others, only about "pass to the next one or don't"

Do **not** use when:
- Exactly one handler always applies — just call it directly, a chain of one is a chain in name only
- Handlers actually need to *combine* their results rather than short-circuit — that's closer to a pipeline/reduce than Chain of Responsibility

## Template

```python
from typing import Protocol

class Handler(Protocol):
    def handle(self, request: Request) -> Response | None: ...

class AuthHandler:
    def __init__(self, next_handler: Handler | None) -> None:
        self._next = next_handler

    def handle(self, request: Request) -> Response | None:
        if not request.token:
            return Response(401, "unauthorized")
        return self._next.handle(request) if self._next else None

class RateLimitHandler:
    def __init__(self, next_handler: Handler | None) -> None:
        self._next = next_handler

    def handle(self, request: Request) -> Response | None:
        if is_rate_limited(request):
            return Response(429, "too many requests")
        return self._next.handle(request) if self._next else None

pipeline = AuthHandler(RateLimitHandler(None))
```

Each handler decides "handle it" or "pass along"; the pipeline's composition (`AuthHandler(RateLimitHandler(None))`) is the only place that knows the order.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Handler interface | `Handler` (`handle(request)`) |
| Concrete handlers | `XxxHandler`, named for the single check/step they own |
| Chain assembly | Composed once at startup/configuration, not rebuilt per request |

## Anti-Patterns

- A handler that mutates the request in a way later handlers don't expect, without documenting it
- Silent request drops — if no handler in the chain handles the request, that should be an explicit, loud outcome, not a `None` that gets ignored
- A chain so long and dynamically reconfigured that debugging "which handler actually fired" requires stepping through every one — keep chains short and log which handler terminated it

## Related Skills

- `design-patterns-catalog` — choosing Chain of Responsibility vs. Decorator (both wrap/forward, but CoR handlers can stop the chain; decorators always call through)
- `mediator-pattern` — centralizing interaction differently: one hub instead of a linear chain
