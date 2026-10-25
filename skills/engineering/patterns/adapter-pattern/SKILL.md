---
name: adapter-pattern
description: >-
  Generic Adapter pattern: convert one interface into another the client
  expects, without modifying either side. Use when wrapping a third-party
  library, a legacy class, or an external API behind the interface your own
  code already depends on. Pair with design-patterns-catalog for picking
  Adapter vs. its neighbors (Facade, Decorator, Bridge).
---

# Adapter Pattern (Portable Template)

Language-agnostic — examples below are Python, but the shape ports directly to any language with interfaces/protocols.

## When to Use

Activate when:
- Integrating a third-party SDK, legacy module, or external API whose interface doesn't match what your code already depends on
- You want your domain/business code to depend on *your own* interface, not on a vendor's shape, so swapping vendors later touches one file
- Two parts of the same codebase evolved incompatible shapes for the same concept (old `UserRecord` vs. new `UserDTO`) and a rewrite of both isn't justified yet
- Writing a test double that must satisfy an interface but wraps a different underlying implementation (fake, in-memory client)

Do **not** use when:
- You own both sides of the interface mismatch — change the callee's interface directly instead of adapting around it forever
- The "adaptation" is a single field rename — a one-line mapping at the call site is simpler than a whole adapter class
- You actually need to *add* behavior (caching, logging, retry) rather than *translate* shape — that's Decorator or Proxy, not Adapter (see `design-patterns-catalog`)

## Two Ways to Implement It

| Variant | When | Cost |
|---|---|---|
| **A. Object adapter** (wraps an instance) | Default choice; works even when you can't subclass the adaptee | One extra indirection layer, composition-based |
| **B. Class adapter** (inherits from the adaptee) | Language supports multiple inheritance/mixins and the adaptee is designed to be subclassed | Tighter coupling to adaptee's implementation, not just its interface |

Prefer **object adapter** (composition) by default — it works with sealed/final classes and doesn't leak the adaptee's implementation details.

## Variant A — Object Adapter

```python
from typing import Protocol

# The interface your own code already depends on
class PaymentGateway(Protocol):
    def pay(self, amount: float, currency: str) -> str: ...

# Third-party/legacy class you don't control, with an incompatible interface
class LegacyXmlPaymentGateway:
    def send_payment_xml(self, xml_payload: str) -> str: ...

class LegacyGatewayAdapter:
    def __init__(self, legacy: LegacyXmlPaymentGateway) -> None:
        self._legacy = legacy

    def pay(self, amount: float, currency: str) -> str:
        xml = f"<pay amount='{amount}' currency='{currency}'/>"
        return self._legacy.send_payment_xml(xml)

def checkout(gateway: PaymentGateway, amount: float) -> str:
    return gateway.pay(amount, currency="USD")

checkout(LegacyGatewayAdapter(LegacyXmlPaymentGateway()), 42.0)
```

`checkout` depends only on `PaymentGateway`. Swap in a real gateway, a new vendor, or a test fake — the adapter is the single place that knows the legacy XML shape exists.

## Variant B — Class Adapter

```python
class StringNormalizer:
    def normalize(self, text: str) -> str:
        return text.strip().lower()

# Adaptee designed to be extended, in a language where this composes cleanly
class LegacyTextCleaner:
    def clean_text(self, raw: str) -> str:
        return raw.replace("\t", " ")

class LegacyCleanerAdapter(LegacyTextCleaner):
    def normalize(self, text: str) -> str:
        return self.clean_text(text).strip().lower()
```

Only reach for this when composition is awkward (e.g. the adaptee expects to be subclassed and exposes protected hooks) — it's the less common case.

## Two-Way Adapter (bridging both directions)

When two subsystems each expect to call the other, implement both interfaces on one adapter so either side can call through it — useful when migrating incrementally between an old and new API and some callers haven't moved yet.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Target interface | Named for the *role*, not the vendor (`PaymentGateway`, not `StripeInterface`) |
| Adapter class | `XxxAdapter` (`LegacyGatewayAdapter`, `StripeGatewayAdapter`) |
| Constructor arg | The wrapped instance, stored as `self._legacy` / `self._client` / `self._wrapped` |

## Anti-Patterns

- Adapter that leaks adaptee-specific types through its return values — defeats the point; translate all the way to the target interface's own types
- Business logic living inside the adapter (retries, validation, defaulting) — the adapter's only job is shape translation; put logic in a decorator or the caller
- One adapter trying to satisfy multiple unrelated target interfaces — split by interface, not by adaptee
- Adapting an interface you actually own — fix the interface instead of adapting around it indefinitely

## Related Skills

- `design-patterns-catalog` — choosing Adapter vs. Facade vs. Decorator vs. Bridge
- `codebase-design` — the seam/adapter vocabulary this pattern is a concrete instance of
- `clean-code` — keeping the adapter itself a thin, single-purpose translation layer
