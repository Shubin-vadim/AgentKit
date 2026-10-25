---
name: architecture-styles
description: >-
  Choose a system-level architecture style (modular monolith, services,
  hexagonal ports/adapters, event-driven, CQRS) with explicit trade-offs, then
  record it as an ADR. Use when the user asks monolith vs microservices,
  hexagonal, event-driven, which architecture pattern, or how to slice the
  system.
---

# Architecture styles

Pick a **style** for the system (or one bounded context), not a library. The output is a recommendation plus an ADR via [adr-write](../adr-write/SKILL.md). Draw the resulting containers with [c4-diagrams](../c4-diagrams/SKILL.md).

Default for a small team / unclear domain: **modular monolith**. Extract a process only when a real force exists (scale, team, technology, failure isolation).

## Forces (ask once if missing)

- Team size and deploy independence
- Domain boundaries (are they stable?)
- Data: one database acceptable vs strict isolation
- Scale: one axis that actually differs (CPU-heavy worker vs chatty API)
- Consistency: single transaction vs eventual
- Ops budget: queues, tracing, many deploys

## Styles

| Style | Use when | Cost |
|-------|----------|------|
| **Modular monolith** | 1–10 people, boundaries still moving, one deploy is fine | Discipline of module seams; easy to cheat imports |
| **Modular monolith + async worker** | work takes minutes / must not block HTTP | Extra process + queue (often the right first split) |
| **Hexagonal (ports & adapters)** | core must run without web/DB (CLI, tests, eval) | Two models at the seam (pydantic vs ORM) |
| **Services** | independent deploy *and* data *and* team ownership | Network, ops, distributed failure |
| **Event-driven** | multiple consumers, time-decoupled, you can accept eventual consistency | ordering, dual-write, debugging |
| **CQRS / event sourcing** | audit/temporal queries, very different read/write scale | Not for simple CRUD or inexperienced teams |

Hexagonal **composes** with a monolith or with services. It is a seam style, not a deploy style. Example: a monorepo where `backend/core/` is a pure library and one service is the only bridge to the web layer is hexagonal inside a monolith.

## Workflow

1. Name the forces in one short list.
2. Eliminate styles that violate a non-negotiable (compliance, team size, latency).
3. Rank two survivors. State the **trade-off point** (what you give up).
4. Write the ADR (Decision = enforceable rules: import bans, who owns the DB, sync vs async).
5. Update C2/C3 to match. If C2 still looks like a class diagram, the style is not visible yet.

## Anti-patterns

- Microservices because "we might need to scale"
- Event sourcing for a CRUD admin
- Hexagonal theater: interfaces with a single adapter forever and no test through the port
- Style chosen in chat and never written as an ADR
