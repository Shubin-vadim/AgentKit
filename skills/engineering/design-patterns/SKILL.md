---
name: design-patterns
description: >-
  Core design patterns for Python service backends: Singleton and Factory. Use when the user
  asks which pattern to apply, how to add a shared service or graph, or mentions
  singleton / factory / XxxFactory.
metadata:
  version: '1.0.0'
paths:
  - src/**
allowed-tools: Read Edit Write
context: fork
---

# Design Patterns

Two patterns cover almost all new infrastructure in a service backend. Open the dedicated skill before writing code.

| Pattern | When | Skill | Examples |
|---------|------|-------|----------|
| **Singleton** | One instance per process (pool, LLM, compiled graph) | `singleton-pattern` | `RAGServiceFactory`, `RedisFactory` |
| **Factory** | Class that **builds and holds** that instance | `factory-pattern` | `AgentGraphFactory`, `PostgresCheckpointerFactory` |

Factory **holds** the singleton; the service/graph **does the work**.

## Rules

- Pools, compiled graphs, embedding/LLM clients → `XxxFactory` + `init()` in the app lifespan (or lazy `get_instance()` if the singleton skill says so).
- Request-scoped state (`AsyncSession`, per-turn runtime services) → FastAPI `Depends()` or LangGraph `configurable`. **Never** store on the factory.
- SQL stays in `*Repository`; routes/handlers call services.

## Related

- `langgraph-fundamentals` — nodes/edges inside a graph factory
