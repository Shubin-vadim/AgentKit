---
name: builder-pattern
description: >-
  Generic Builder pattern: construct a complex object step by step, same
  construction process, different representations. Use when a constructor
  would need many optional/order-dependent parameters, or when an object must
  be assembled over several validated steps, in any language or project.
---

# Builder Pattern (Portable Template)

## When to Use

Activate when:
- A constructor's parameter list is long, mostly optional, and combinations of them are order- or validity-dependent
- The object passes through invalid intermediate states during assembly that you want to make unrepresentable to callers (partially-built requests, documents, queries)
- You want a fluent, readable call chain instead of a wall of keyword arguments

Do **not** use when:
- There are only 2–3 fields — a dataclass, record, or plain keyword arguments already reads clearly and needs no extra type
- The construction process is a single step with no ordering or validity constraints between parts

## Template

```python
class HttpRequestBuilder:
    def __init__(self) -> None:
        self._method = "GET"
        self._headers: dict[str, str] = {}
        self._body: str | None = None

    def method(self, method: str) -> "HttpRequestBuilder":
        self._method = method
        return self

    def header(self, key: str, value: str) -> "HttpRequestBuilder":
        self._headers[key] = value
        return self

    def body(self, body: str) -> "HttpRequestBuilder":
        self._body = body
        return self

    def build(self) -> HttpRequest:
        if self._method in {"POST", "PUT"} and self._body is None:
            raise ValueError(f"{self._method} requires a body")
        return HttpRequest(self._method, self._headers, self._body)

request = (
    HttpRequestBuilder()
    .method("POST")
    .header("Content-Type", "application/json")
    .body('{"a": 1}')
    .build()
)
```

Validation lives in `build()`, run once, at the point where the object becomes real — not scattered across every setter.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Builder class | `XxxBuilder` |
| Step methods | Verb or noun matching the field they set (`method(...)`, `header(...)`), return `self` for chaining |
| Terminal method | `build()` — the only method that can raise on invalid combinations and the only one returning the final product |

## Anti-Patterns

- A builder whose `build()` never validates anything — if there's nothing to protect against, you don't need a builder, use a constructor
- Step methods that mutate the already-built product instead of internal builder state, breaking reuse of the same builder for multiple products
- A "builder" with no fluent chaining and no validation — that's just a mutable struct with extra ceremony

## Related Skills

- `design-patterns-catalog` — choosing Builder vs. Factory Method vs. plain constructor
- `clean-code` — long-parameter-list smell that Builder is one valid fix for (a parameter object is often simpler when there's no step-order constraint)
