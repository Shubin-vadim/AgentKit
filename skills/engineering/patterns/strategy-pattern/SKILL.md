---
name: strategy-pattern
description: >-
  Generic Strategy pattern: encapsulate interchangeable algorithms behind one
  shared interface, swap the implementation at runtime. Use when adding
  pluggable behavior (pricing rule, sort order, auth scheme, retry policy,
  discount calculation) in any language or project. Pair with
  design-patterns-catalog for picking Strategy vs. its neighbors (State,
  Template Method).
---

# Strategy Pattern (Portable Template)

Language-agnostic — examples below are Python, but the shape ports directly to any language with interfaces/protocols/first-class functions.

## When to Use

Activate when:
- Several interchangeable ways exist to do the same job, selected by caller, config, or user choice (pricing rule, sort comparator, compression algorithm, auth scheme)
- A method is growing a long `if`/`elif`/`switch` on a "kind" or "mode" parameter, and each branch is a self-contained algorithm
- You need to swap the algorithm at runtime, or inject a fake/no-op one in tests, without touching the calling code
- The variants share the same inputs/outputs but differ in *how* they compute the result

Do **not** use when:
- There is exactly one algorithm today and no concrete second one on the horizon — you're building an interface for a variant that doesn't exist yet
- The "variants" are really just 2 branches of a single `if` — a plain conditional is more readable than an interface plus two classes
- The behavior differs by *object identity/state* over time rather than by *algorithm choice* — that's State, not Strategy (see `design-patterns-catalog`)

## Two Ways to Implement It

| Variant | When | Cost |
|---|---|---|
| **A. Class-based** (one class per strategy) | Strategy needs its own state/config, or has multiple methods | More boilerplate, but scales to complex strategies |
| **B. Function-based** (plain callables) | Strategy is stateless, a single pure computation | Minimal boilerplate — prefer this by default in languages with first-class functions |

## Variant A — Class-Based Strategy

```python
from typing import Protocol

class PricingStrategy(Protocol):
    def price(self, base: float) -> float: ...

class RegularPricing:
    def price(self, base: float) -> float:
        return base

class BlackFridayPricing:
    def price(self, base: float) -> float:
        return base * 0.6

class LoyaltyPricing:
    def __init__(self, discount_rate: float) -> None:
        self._discount_rate = discount_rate

    def price(self, base: float) -> float:
        return base * (1 - self._discount_rate)

class Cart:
    def __init__(self, strategy: PricingStrategy) -> None:
        self._strategy = strategy

    def total(self, base: float) -> float:
        return self._strategy.price(base)
```

Use a class when the strategy needs constructor-injected config (`LoyaltyPricing(discount_rate=0.1)`) or exposes more than one related method.

## Variant B — Function-Based Strategy

```python
from typing import Callable

PricingStrategy = Callable[[float], float]

def regular_pricing(base: float) -> float:
    return base

def black_friday_pricing(base: float) -> float:
    return base * 0.6

def loyalty_pricing(discount_rate: float) -> PricingStrategy:
    def _price(base: float) -> float:
        return base * (1 - discount_rate)
    return _price

def checkout_total(base: float, strategy: PricingStrategy) -> float:
    return strategy(base)

checkout_total(100, black_friday_pricing)          # 60.0
checkout_total(100, loyalty_pricing(0.1))           # 90.0
```

Prefer this by default — no interface ceremony, and it composes naturally with `functools.partial` or closures for configured variants.

## Selecting a Strategy at the Edge

Keep the *selection* logic (config lookup, `if`/dict dispatch) in exactly one place — a factory function or a registry — not scattered across callers:

```python
STRATEGIES: dict[str, PricingStrategy] = {
    "regular": regular_pricing,
    "black_friday": black_friday_pricing,
}

def get_pricing_strategy(name: str) -> PricingStrategy:
    try:
        return STRATEGIES[name]
    except KeyError:
        raise ValueError(f"unknown pricing strategy: {name}")
```

Callers ask for a strategy by name once, then use it as a plain value — they never re-derive the mapping themselves.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Interface/protocol | `XxxStrategy` (`PricingStrategy`, `SortStrategy`) |
| Class-based implementation | `RegularPricing`, `BlackFridayPricing` — named for the *variant*, not suffixed `...StrategyImpl` |
| Function-based implementation | `regular_pricing`, `black_friday_pricing` — verb/noun phrase, no `Strategy` suffix needed |
| Selector | `get_xxx_strategy(name)` or a `XXX_STRATEGIES` registry dict |

## Anti-Patterns

- A `StrategyContext` class that just forwards one call to the strategy and does nothing else — delete it, call the strategy directly
- Strategy classes that reach back into the caller's internals instead of taking everything they need as method arguments
- One "God strategy" interface with 10 methods where callers only ever need one — split by actual use, or fall back to plain functions
- Re-deriving the `if name == "x": return XStrategy()` dispatch in more than one place instead of a single registry/factory

## Related Skills

- `design-patterns-catalog` — choosing Strategy vs. State vs. Template Method
- `clean-code` — command-query separation and small-function guidance that keeps individual strategies focused
