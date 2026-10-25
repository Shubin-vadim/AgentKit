---
name: python-code-style
description: >-
  Mandatory Python code style for this project: Pydantic over dataclass,
  Sphinx-style English docstrings, one class per file, English-only
  comments, required design patterns, full type hints, SOLID, OOP-first
  features, a shared utils.py for standalone helpers, and DRY/KISS/YAGNI.
  Use whenever writing or reviewing Python code in this repo — not a style
  suggestion, a checklist to enforce.
metadata:
  version: '2.0.0'
paths:
  - src/**
allowed-tools: Read Edit Write
context: fork
---

# Python Code Style

Twenty-one binding rules for this codebase. Not general Python advice — apply exactly as written; deviations need an explicit reason in review, not a stylistic preference.

Wrong/right code for each rule: [references/examples.md](references/examples.md) (sections numbered like the rules). Open it when writing or reviewing code for a specific rule.

## 1. Pydantic models, never `dataclass`

Every structured data object is a `pydantic.BaseModel` (or `pydantic.BaseSettings`/its v2 equivalent for config). Do not use `@dataclass`, `NamedTuple`, or a bare class with manually written `__init__` for data containers.

Example: [references/examples.md](references/examples.md) § 1.

**Why:** one validation/serialization story across the codebase — no second type system to keep in sync with FastAPI's request/response models.

## 2. Docstrings: English only, Sphinx style for callables

- **Classes**: one short English sentence describing what the class is/does. No Sphinx fields on the class docstring itself.
- **Functions/methods**: Sphinx-style docstring — `:param:`, `:return:`, `:raises:` — for every function that has parameters, a return value, or can raise. English only, no exceptions.

Example: [references/examples.md](references/examples.md) § 2.

Skip the docstring only for trivial one-line `__init__` bodies that just assign constructor args with no logic — everything else gets one.

## 3. One class per file (except cohesive Pydantic model groups)

A file holds exactly one class with real behavior. Do not stack multiple unrelated classes in one module.

**Exception:** a set of Pydantic models that are semantically one concept (a request/response family, e.g. `OrderCreate`/`OrderUpdate`/`OrderResponse`) may live together in one `schemas.py`/`models.py`, because they're data, not independent behavior.

Example: [references/examples.md](references/examples.md) § 3.

## 4. Comments: English only

Every comment in the codebase is in English, no exceptions, regardless of the team's spoken language. Follow `clean-code` for *when* to comment (why, not what) — this rule only fixes the language.

## 5. Design patterns are mandatory where a pattern applies

Before implementing new functionality, name the applicable pattern and use it — don't default to ad hoc procedural code when a known shape fits. Consult `design-patterns-catalog` to pick the right one, and this repo's `design-patterns` / `singleton-pattern` / `factory-pattern` for shared services and singletons.

This does not mean forcing a pattern where none fits — `design-patterns-catalog`'s "Don't use when" column still applies. It means: check the catalog before writing a bespoke solution to a problem that already has a named shape (pluggable behavior → Strategy, wrapping a vendor SDK → Adapter, shared process-wide resource → Singleton, and so on).

## 6. Full type annotations everywhere

Every function signature, method, and variable whose type isn't obvious from the right-hand side is annotated. No untyped `def`, no bare `**kwargs` without a `TypedDict`/`Unpack` where feasible, no `Any` used to avoid figuring out the real type.

Example: [references/examples.md](references/examples.md) § 6.

Run/require the project's type checker (mypy/pyright) as a real gate, not a suggestion.

## 7. SOLID

- **S**ingle Responsibility — one class, one reason to change (this is also why rule 3 exists).
- **O**pen/Closed — extend via new classes/strategies, not by editing a growing `if/elif` chain in an existing one.
- **L**iskov Substitution — a subclass must be usable anywhere its base type is expected, without surprising the caller.
- **I**nterface Segregation — depend on small, specific `Protocol`s, not one fat interface nobody fully implements.
- **D**ependency Inversion — depend on abstractions (`Protocol`, injected `Depends()`), not concrete implementations, at module boundaries.

## 8. Features are implemented via OOP

New functionality is expressed as classes with clear responsibilities and interfaces — not as a script-like sequence of module-level function calls mutating shared globals. A feature gets a service/class with a clear public interface; internal steps are private methods.

## 9. Standalone helper functions live in `utils.py`

A function needed by the feature but that doesn't belong to any class (pure helpers: formatting, small conversions, stateless calculations reused across classes) goes in that module's `utils.py`, not scattered as loose functions across unrelated files or bolted onto a class that doesn't own them.

Example: [references/examples.md](references/examples.md) § 9.

If a "utility" function starts needing state or several related helpers with shared config, it has outgrown `utils.py` — turn it into a class instead (see rule 8).

## 10. DRY, KISS, YAGNI

- **DRY** — extract shared logic once a third real duplicate appears; don't copy-paste a third time.
- **KISS** — prefer the plainest implementation that satisfies the requirement; no cleverness that isn't earning its keep.
- **YAGNI** — don't build configurability, abstraction layers, or patterns for a requirement that doesn't exist yet; this includes not pre-applying a design pattern from rule 5 where `design-patterns-catalog` says "don't use when."

## 11. Tooling: Ruff for format + lint, line-length 88

Ruff is the single formatter and linter — no separate Black/isort/flake8/pylint stack. CI runs `ruff format --check` and `ruff check` as hard gates, not advisory.

```toml
# ruff.toml (or [tool.ruff] in pyproject.toml)
line-length = 88
target-version = "py312"

[format]
quote-style = "double"

[lint]
select = ["E", "F", "I", "B", "C90", "PL", "UP"]
[lint.pylint]
max-args = 4
max-branches = 12
[lint.mccabe]
max-complexity = 10
[lint.isort]
combine-as-imports = true
known-first-party = ["src"]
```

## 12. Naming conventions beyond PEP 8

| Kind | Rule | Example |
|---|---|---|
| Private attribute/method | Leading `_`, always — nothing outside the class's own public interface skips it | `self._connection`, `def _validate(self)` |
| Module-level constant | `UPPER_SNAKE_CASE`, no magic values inline | `MAX_RETRIES = 3` |
| `Protocol`/interface | Suffix `Protocol` | `class PaymentGatewayProtocol(Protocol): ...` |
| Custom exception | Suffix `Error` | `class OrderNotFoundError(AppError): ...` |

## 13. Exception handling policy

- Maintain one exception hierarchy per domain, rooted in a project-wide `AppError`, instead of raising bare `ValueError`/`RuntimeError` for domain failures (`OrderError(AppError)`, `PaymentError(AppError)`, then specific `OrderNotFoundError(OrderError)`).
- Never write `except Exception:` (or bare `except:`) without either re-raising or logging with full context — catch only what you can actually handle at that layer.
- Every exception message states the concrete context: what value, what operation, what was expected — not a generic `"invalid input"`.
- Log the error at the point where it crosses a layer boundary (service → API), right before it's raised or translated into an HTTP response, so the log has the causal context, not just the final response.

Example: [references/examples.md](references/examples.md) § 13.

## 14. Logging: one logger per module, no `print()`

Every module that logs declares `logger = logging.getLogger(__name__)` at the top. `print()` is never used for anything other than a CLI's own user-facing output.

Example: [references/examples.md](references/examples.md) § 14.

## 15. String quotes: double quotes only

Use `"double quotes"` for all string literals, project-wide, with no mixed style. This is enforced by Ruff's `quote-style = "double"` (rule 11) — don't hand-pick single quotes even where it would avoid escaping; escape instead.

## 16. Async: mandatory for I/O, no blocking calls inside `async def`

Any I/O-bound operation (HTTP call, DB query, file read, sleep) inside an `async def` uses its async counterpart — `httpx.AsyncClient` not `requests`, `asyncio.sleep` not `time.sleep`, an async DB driver not a sync one. A blocking call inside an async function stalls the whole event loop, not just that request.

Example: [references/examples.md](references/examples.md) § 16.

## 17. Tests: a unit test for every public method

Every public method on every class gets at least one unit test covering its main path; add more for each distinct branch/edge case. A class without test coverage for its public interface isn't done — this is a style/definition-of-done rule, not a separate testing skill's concern (pair with `tdd` for how to write the tests themselves).

## 18. Function/method size and argument-count limits, enforced by the linter

Target ≤ ~50 lines per function/method and ≤ 4 positional parameters — enforced through Ruff (`max-args`, `mccabe` complexity in rule 11's config), not left to reviewer judgment. Once a function needs a 5th parameter, introduce a Pydantic parameter object instead of adding another positional argument.

Example: [references/examples.md](references/examples.md) § 18.

## 19. Imports

- Absolute imports only — never `from . import x` or `from .. import y`. Absolute imports keep working unchanged when a file moves.
- No wildcard imports (`from module import *`) — every imported name must be traceable to its origin.
- Group and order: standard library → third-party → local (`src`), alphabetical within each group — enforced by Ruff's `isort` rules (rule 11's config).
- No circular imports between modules — if module A imports from B and B imports from A, the boundary between them is wrong; extract the shared piece into a third module or invert the dependency (see rule 21).

## 20. Immutability and state

- Value-object/DTO Pydantic models default to immutable: `model_config = ConfigDict(frozen=True)` wherever the object isn't meant to be mutated after construction (most request/response and domain-value models qualify; models representing something actively edited in place, e.g. an in-progress form builder, are the explicit exception).
- Never use a mutable default argument (`def f(x: list = [])`). Default to `None` and initialize inside the function body.
- Services and repositories never hold request-scoped state on `self` between calls — that state is passed explicitly through method arguments (or `RunnableConfig.configurable` where LangGraph is involved), never stashed as an instance attribute that leaks between requests.

Example: [references/examples.md](references/examples.md) § 20.

## 21. Structure and dependency direction

- Every package has an `__init__.py` with an explicit, `__all__`-declared re-export of its public API — callers import from the package, not by reaching into its internal modules.
- Dependencies flow one way: `api` → `service` → `repository`. A repository never imports from a service; a service never imports from the API layer. If a lower layer needs something from a higher one, invert the dependency (pass it in, or move the shared piece down) instead of adding a backward import.
- SQL/query code lives only in `*Repository` classes; business logic lives only in `*Service` classes — a service never builds a raw query, a repository never makes a business decision.

## Review Checklist

- [ ] No `@dataclass`/`NamedTuple` used for structured data — Pydantic only
- [ ] Every class has a one-line English docstring; every non-trivial function has a Sphinx-style English docstring
- [ ] One class per file, except cohesive Pydantic model groups
- [ ] All comments are in English
- [ ] A named design pattern backs any non-trivial new behavior, or its absence is justified
- [ ] Full type hints on every signature; type checker passes
- [ ] SOLID isn't violated (no god classes, no editing closed code with new `if` branches, `Protocol`s at boundaries)
- [ ] New feature is a class with a clear interface, not a loose script
- [ ] Standalone helpers are in `utils.py`, not orphaned or misfiled
- [ ] No duplicated logic (3rd occurrence unextracted), no speculative abstraction, no unused flexibility
- [ ] `ruff format --check` and `ruff check` pass (line-length 88, double quotes, isort, max-args, complexity)
- [ ] Naming: `_private`, `UPPER_SNAKE_CASE` constants, `XxxProtocol`, `XxxError`
- [ ] Domain exceptions extend a project `AppError` hierarchy; no unhandled bare `except Exception`; messages carry context; boundary-layer logging before raise/translation
- [ ] Every module that logs uses `logger = logging.getLogger(__name__)`; no `print()`
- [ ] All string literals use double quotes
- [ ] No blocking I/O calls inside `async def`
- [ ] Every public method has at least one unit test
- [ ] No function/method exceeds ~50 lines or 4 positional args without a parameter object
- [ ] Imports are absolute, non-wildcard, grouped/sorted, and acyclic
- [ ] Value/DTO models are `frozen` where appropriate; no mutable default arguments; no request-scoped state on `self`
- [ ] `__init__.py` re-exports the package's public API explicitly; dependencies flow `api → service → repository` only; SQL stays in `*Repository`, business logic in `*Service`

## Related Skills

- `clean-code` — general readability principles this style sheet specializes for this codebase
- `design-patterns-catalog`, `design-patterns`, `singleton-pattern`, `factory-pattern` — pattern selection referenced by rule 5
- `tdd` — how to write the unit tests rule 17 requires
- `dependency-injection` — how rule 7's Dependency Inversion is actually wired: constructor injection, `Protocol`s, FastAPI `Depends()`
