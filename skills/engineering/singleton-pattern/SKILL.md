---
name: singleton-pattern
description: >-
  Reusable process-wide singleton patterns for FastAPI/Python backends: explicit-init
  factories, lazy get_instance(), @lru_cache clients, reset/dispose lifecycle. Use
  when adding shared services, API clients, or wiring lifespan in any project.
  Pair with factory-pattern for XxxFactory classes.
metadata:
  version: '1.0.0'
paths:
  - src/**
  - src/main.py
allowed-tools: Read Edit Write
context: fork
---

# Singleton Pattern (Portable Template)

Reusable across projects.

## When to Use

Activate when:
- Adding a new process-wide service (DB pool, Redis, LLM, embedding model, HTTP client)
- Refactoring duplicated initialization into a single instance
- Wiring FastAPI `Depends()` for a shared resource
- Deciding between explicit startup init vs lazy first-use creation

Do **not** use singleton for **per-request** or **per-thread** state (per-conversation runtime services, `RunnableConfig.configurable`, repository sessions).

## Three Variants

| Variant | When | Examples |
|---------|------|----------|
| **A. Explicit init** | Heavy/ordered startup; must fail fast if not ready | `PostgresServiceFactory`, `RAGServiceFactory`, `RedisFactory`, `PromptServiceFactory` |
| **B. Lazy first use** | Cheap or self-contained; no strict startup order | `LLMServiceFactory`, `EmbeddingServiceFactory`, `PostgresCheckpointerFactory` |
| **C. `@lru_cache`** | Stateless HTTP API clients | `get_payments_api_client()` in `clients/dependencies.py` |

## Variant A — Explicit Init (preferred for infra)

```python
class FooServiceFactory:
    _instance: FooService | None = None

    @classmethod
    def init(cls, ...) -> FooService:
        cls._instance = FooService(...)
        return cls._instance

    @classmethod
    def get_instance(cls) -> FooService:
        if cls._instance is None:
            raise RuntimeError(
                "FooService is not initialized. Call FooServiceFactory.init() during application startup."
            )
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Shutdown or tests only."""
        cls._instance = None
```

Rules:
- Call `init()` from `lifespan` in the app entry point in dependency order
- `get_instance()` **never** creates — only raises `RuntimeError`
- Add `reset()` when shutdown or tests need cleanup
- Export `get_foo_service()` + `FooServiceDep = Annotated[FooService, Depends(get_foo_service)]`

## Variant B — Lazy First Use

```python
class BarServiceFactory:
    _instance: BarService | None = None

    @classmethod
    def get_instance(cls) -> BarService:
        if cls._instance is None:
            cls._instance = BarService(deps...)
        return cls._instance
```

Use when:
- Initialization is idempotent and inexpensive
- Service can be created on first HTTP request without lifespan entry

Still add `get_bar_service()` + `BarServiceDep` for FastAPI routes.

## Variant C — `@lru_cache` for API Clients

```python
@lru_cache
def get_payments_api_client() -> PaymentsAPIClient:
    return PaymentsAPIClient()

PaymentsAPIClientDep = Annotated[PaymentsAPIClient, Depends(get_payments_api_client)]
```

Use for thin HTTP wrappers in `clients/`. Do **not** use for DB pools, LangGraph graphs, or services with `dispose()`.

## Lifespan Integration

Typical startup order (simplified):

1. `setup_checkpointer()` → `PostgresCheckpointerFactory`
2. `PostgresServiceFactory.init_postgres_service()`
3. `RedisFactory.init()`
4. Services that need Redis → `PromptServiceFactory.init(redis_service)`
5. Expensive ML/vector → `RAGServiceFactory.init_rag_service()`
6. Dependent caches → `AnswerCacheServiceFactory.init(...)`
7. LangGraph factories → `ClassifierGraphFactory.init(...)`, `AgentGraphFactory.init(...)`

Shutdown (reverse): dispose pools → `Factory.reset()` where defined.

## Checklist for New Singleton

- [ ] Choose variant A, B, or C (see table above)
- [ ] Class name: `XxxFactory` or `@lru_cache get_xxx()` in `dependencies.py`
- [ ] Module-level `get_xxx()` returning singleton
- [ ] `XxxDep = Annotated[Xxx, Depends(get_xxx)]` for routes/services
- [ ] If variant A: `init()` in `lifespan` + `reset()`/`dispose()` in `finally`
- [ ] Re-export from the package `__init__.py` if public
- [ ] Error message names the required `init()` call
- [ ] Do **not** store per-request state on the singleton

## Anti-Patterns

- Creating singleton inside route handler without factory guard
- Mixing `init()` and lazy creation in the same factory (`get_instance` must be consistent)
- Using singleton for LangGraph **runtime** deps (pass via `configurable`)
- Forgetting shutdown for connection pools (asyncpg, psycopg, Redis)

## Related Skills

- **design-patterns** — when to pick singleton vs factory
- **factory-pattern** — `XxxFactory`, graph factories, `get_or_create`
- **dependency-injection** — how the singleton reaches consumers: constructor injection against a `Protocol`, wired through `Depends()`
