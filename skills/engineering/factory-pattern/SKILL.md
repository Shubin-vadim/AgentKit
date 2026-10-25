---
name: factory-pattern
description: >-
  Reusable factory pattern for FastAPI backends: XxxFactory building singletons
  (services, compiled graphs, pools), init/get_instance/get_or_create, FastAPI
  Depends bridges. Use in any project when creating FooServiceFactory or
  GraphFactory. Pair with singleton-pattern for lifecycle rules.
metadata:
  version: '1.0.0'
paths:
  - src/**
  - src/main.py
allowed-tools: Read Edit Write
context: fork
---

# Factory Pattern (Portable Template)

Reusable across projects.

## When to Use

Activate when:
- Creating `XxxFactory` to build a heavy object once (service, graph, pool)
- Adding a new LangGraph orchestrator (`StateGraph` → `compile`)
- Centralizing construction logic with injected dependencies
- Exposing compiled graphs or services via `Depends()`

Factory **holds** the singleton; the service/graph class **does the work**.

## Factory Types

| Type | Builds | Init style | Example |
|------|--------|------------|---------|
| **Service factory** | Business/infra service | `init_*()` in lifespan | `RAGServiceFactory`, `RedisFactory` |
| **Graph factory** | `CompiledStateGraph` | `init()` startup or `get_or_create()` lazy | `AgentGraphFactory`, `RAGGraphFactory` |
| **Resource factory** | Pool + derived resource | Lazy `get_instance()` | `PostgresCheckpointerFactory` |

## Service Factory Template

Place next to the service class (same module or `service.py`).

```python
class FooService:
    def __init__(self, ...) -> None:
        ...

class FooServiceFactory:
    _instance: FooService | None = None

    @classmethod
    def init(cls, ...) -> FooService:
        cls._instance = FooService(...)
        logger.info("FooService initialized")
        return cls._instance

    @classmethod
    def get_instance(cls) -> FooService:
        if cls._instance is None:
            raise RuntimeError("FooService not initialized. Call FooServiceFactory.init() during application startup.")
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        cls._instance = None


def get_foo_service() -> FooService:
    return FooServiceFactory.get_instance()


FooServiceDep = Annotated[FooService, Depends(get_foo_service)]
```

## LangGraph Factory Template

Place next to the graph package (for example `<orchestrators>/<name>/graph.py`).

```python
XxxCompiledGraph = CompiledStateGraph[XxxState, None, XxxState, XxxState]


class XxxGraphFactory:
    _instance: XxxGraphFactory | None = None

    def __init__(self, llm_service: LLMService, *, use_checkpointer: bool = True) -> None:
        self._graph = self._build_graph(llm_service, use_checkpointer=use_checkpointer)

    def _build_graph(self, llm_service: LLMService, *, use_checkpointer: bool) -> XxxCompiledGraph:
        builder = StateGraph[XxxState, None, XxxState, XxxState](XxxState)
        # add_node, add_edge, add_conditional_edges ...
        saver = get_postgres_checkpointer() if use_checkpointer else None
        compiled = builder.compile(checkpointer=saver)
        handler = get_langfuse_handler()
        if handler is not None:
            compiled = compiled.with_config({"callbacks": [handler], "metadata": {"langfuse_tags": ["xxx_graph"]}})
        return compiled

    def get_graph(self) -> XxxCompiledGraph:
        return self._graph

    @classmethod
    def init(cls, llm_service: LLMService, *, use_checkpointer: bool = True) -> XxxGraphFactory:
        cls._instance = cls(llm_service=llm_service, use_checkpointer=use_checkpointer)
        return cls._instance

    @classmethod
    def get_or_create(cls, llm_service: LLMService, *, use_checkpointer: bool = True) -> XxxGraphFactory:
        if cls._instance is None:
            cls._instance = cls(llm_service=llm_service, use_checkpointer=use_checkpointer)
        return cls._instance

    @classmethod
    def get_instance(cls) -> XxxGraphFactory:
        if cls._instance is None:
            raise RuntimeError("XxxGraphFactory not initialized. Call init() or get_or_create() first.")
        return cls._instance


def get_xxx_graph(llm_service: LLMServiceDep, ...) -> XxxCompiledGraph:
    return XxxGraphFactory.get_or_create(llm_service=llm_service, ...).get_graph()


XxxGraphDep = Annotated[XxxCompiledGraph, Depends(get_xxx_graph)]
```

### Graph factory: `init` vs `get_or_create`

| Method | Use when |
|--------|----------|
| `init()` | Graph must exist at startup (`main.py` lifespan) — e.g. agent, classifier |
| `get_or_create()` | First request builds graph with injected deps — RAG graph |
| `get_instance()` | After init; used by `get_*_graph()` when startup already called `init()` |

## Multi-Resource Factory (pool + product)

When factory owns connection lifecycle:

```python
class PostgresCheckpointerFactory:
    _instance: PostgresCheckpointerFactory | None = None
    _pool: AsyncConnectionPool | None = None
    _checkpointer: AsyncPostgresSaver | None = None

    def __init__(self) -> None:
        self._pool = AsyncConnectionPool(...)
        self._checkpointer = AsyncPostgresSaver(conn=...)

    @classmethod
    def get_instance(cls) -> PostgresCheckpointerFactory:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_checkpointer(self) -> AsyncPostgresSaver: ...
    async def setup(self) -> None: ...
    async def dispose(self) -> None: ...
```

Expose thin module functions: `get_postgres_checkpointer()`, `setup_checkpointer()`.

## Wiring Checklist

1. **Factory class** with `_instance`, build logic in `__init__` or `init()`
2. **Accessor** `get_instance()` / `get_graph()` / `get_service()`
3. **DI bridge** `get_xxx()` + `XxxDep`
4. **Lifespan** — call `Factory.init(...)` in correct order (app entry point)
5. **Shutdown** — `dispose()`, `reset()`, `_reset_for_tests()` where needed
6. **Package exports** — `__init__.py` re-exports factory + `get_*` + `*Dep`
7. **Tests** — `use_checkpointer=False` or `_reset_for_tests()`; no production singleton leakage

## LangGraph-Specific Rules

- Nodes stay in `nodes/`; edges in `edges/`; factory only wires graph
- Pass **per-invocation** deps via `RunnableConfig.configurable`, not factory fields (user, tenant, or session context)
- Use `get_postgres_checkpointer()` for production; `None` checkpointer in tests
- Attach Langfuse via `compiled.with_config({"callbacks": [handler]})` when handler exists
- Type alias: `XxxCompiledGraph = CompiledStateGraph[State, ...]`

## Naming Conventions

| Artifact | Pattern |
|----------|---------|
| Factory class | `FooServiceFactory`, `AgentGraphFactory` |
| Init method | `init()` or `init_foo_service()` |
| Getter on factory | `get_instance()`, `get_graph()`, `get_checkpointer()` |
| FastAPI injector | `get_foo_service()`, `get_agent_graph()` |
| Dep alias | `FooServiceDep`, `AgentGraphDep` |

## Anti-Patterns

- Business logic inside factory (belongs in service nodes/services)
- Multiple `compile()` calls per process
- Graph factory capturing request-scoped services in `__init__` when they vary per thread
- Skipping `logger.info` on successful factory init (aids ops debugging)

## Related Skills

- **design-patterns** — when to pick singleton vs factory
- **singleton-pattern** — explicit init vs lazy vs `@lru_cache`
- **langgraph-fundamentals** — nodes/edges inside the compiled graph
- **dependency-injection** — how consumers receive the factory's product: constructor injection against `Protocol`s, not concrete-type coupling
