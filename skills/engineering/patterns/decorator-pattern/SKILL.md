---
name: decorator-pattern
description: >-
  Generic Decorator pattern: attach behavior to an object dynamically through
  the same interface it already implements, so decorators stack in any
  combination. Use when adding responsibilities like logging, caching, retry,
  or encryption without a subclass explosion, in any language or project.
---

# Decorator Pattern (Portable Template)

## When to Use

Activate when:
- You need to add responsibilities (logging, caching, retry, encryption, compression) to an object without touching its class
- Several such responsibilities may need to combine, in different combinations, and subclassing for every combination would explode (`CompressedEncryptedSource`, `EncryptedCompressedSource`, ...)
- The added behavior must be transparent to callers — they keep using the same interface whether or not it's decorated

Do **not** use when:
- Only one fixed combination is ever needed — a single class doing both jobs is simpler and easier to read than two stacked decorators
- The "extra behavior" actually changes *what* the object does rather than wrapping *how* it does it — that's more likely Strategy

## Template

```python
from typing import Protocol

class DataSource(Protocol):
    def read(self) -> bytes: ...
    def write(self, data: bytes) -> None: ...

class EncryptionDecorator:
    def __init__(self, wrapped: DataSource) -> None:
        self._wrapped = wrapped

    def read(self) -> bytes:
        return decrypt(self._wrapped.read())

    def write(self, data: bytes) -> None:
        self._wrapped.write(encrypt(data))

class CompressionDecorator:
    def __init__(self, wrapped: DataSource) -> None:
        self._wrapped = wrapped

    def read(self) -> bytes:
        return decompress(self._wrapped.read())

    def write(self, data: bytes) -> None:
        self._wrapped.write(compress(data))

source: DataSource = EncryptionDecorator(CompressionDecorator(FileDataSource("out.bin")))
```

Each decorator implements exactly the interface it wraps (`DataSource`), so any of them can wrap any other, in any order, and the caller never knows the difference.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Shared interface | The role name the decorators and the base implementation all share (`DataSource`) |
| Decorator classes | `XxxDecorator` (`EncryptionDecorator`, `CompressionDecorator`) |
| Constructor arg | The wrapped instance, conventionally `wrapped` or `inner` |

## Anti-Patterns

- A decorator that changes the interface instead of preserving it — that's no longer a decorator, callers can't treat it interchangeably with the undecorated object
- Order-dependent decorators whose correctness silently depends on stacking order with no comment or guard explaining why
- Reaching for decorator stacking when a single function composing two clearly-named steps would be just as readable and far easier to trace

## Related Skills

- `design-patterns-catalog` — choosing Decorator vs. Proxy vs. Adapter vs. Bridge
- `proxy-pattern` — same "same-interface wrapper" shape, but controlling *access* rather than *adding* behavior
- `strategy-pattern` — when the "behavior" actually varies *what* is computed, not just wraps *how* it's delivered
