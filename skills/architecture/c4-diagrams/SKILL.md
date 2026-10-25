---
name: c4-diagrams
description: >-
  Draw C4 architecture diagrams in Mermaid: system context (C1), containers (C2),
  components (C3), ERD instead of code-level C4, plus pipeline and sequence views.
  Use when the user asks for C4, system context, container diagram, component
  diagram, docs/C4.md, architecture diagrams, or how the system is structured.
---

# C4 diagrams

Document **what the system is**. Levels follow the [C4 model](https://c4model.com/). Notation is **Mermaid in `docs/C4.md`**, readable on GitHub with no extra tooling.

Do not use PlantUML unless the repo already has `.puml` as source of truth. Do not invent a `diagrams/` folder for a first draft.

Scaffolds per level: [C4-TEMPLATES.md](C4-TEMPLATES.md).

## File

Write or update `docs/C4.md` (create `docs/` lazily). If it still has `<...>` placeholders, it is the installed template: replace the placeholders and drop its HTML comments. Opening paragraph:

- C1–C3 follow C4
- classic level 4 (code) is replaced by an ERD when the system has a data model
- terms from `CONTEXT.md`
- decisions from `adr/` — link them under the diagram they constrain

Each diagram has a one-line *Audience:* caption (stakeholder / developer / DevOps).

## Vocabulary

Use C4 names, not synonyms:

| Level | Shows | Audience |
|-------|--------|----------|
| **C1 Context** | people + this system + **external** systems | stakeholder |
| **C2 Containers** | separately deployable / runnable pieces | developer, DevOps |
| **C3 Components** | internals of one container, including hard module boundaries | developer |
| **Level 4** | ERD (or skip) — not class diagrams | developer |
| **Runtime** | sequence of the key user path | developer |
| **Pipeline** | ordered steps inside a long-running process | developer |

A **container** is a process or data store you could deploy or crash independently (API, worker, SPA, Postgres, Redis, object storage). A **library** (an HTTP client, a PDF renderer, an SDK) is **not** a C1 system — omit it from context; show it inside C3 if it matters.

Dashed edges = optional, ops-only, or non-blocking (observability that must not fail the happy path).

## Workflow

1. Read `CONTEXT.md` and existing ADRs. Node labels use glossary terms (`Order`, `Cart`, `Invoice`) — never the avoided synonyms.
2. If the user named a scope (one service, one bounded context), draw only that. Otherwise C1 → C2 → C3 in that order; stop when the next level would be guesswork — leave a `TODO:` rather than invent boxes.
3. After a new Accepted ADR that changes structure, update the affected diagram in the same change.
4. Keep diagrams small: one concern per figure. Split pipeline / sequence out of C3.

## Mermaid rules

- `flowchart TB` for C1–C3 and pipelines; `erDiagram` for data; `sequenceDiagram` for the key path.
- `subgraph` for a deployable host (VPS, Docker Compose) or a module boundary (`backend/core/` vs `backend/app/`).
- Node text: emoji + **role** + one-line responsibility. Edge labels: protocol or artifact (`HTTPS`, `SQL`, `enqueue job`).
- Link ADRs in the prose under the diagram, not inside the Mermaid (links inside mermaid break on GitHub).

## Anti-patterns

- C1 stuffed with internal libraries and every SaaS in `requirements.txt`
- C2 that is really a class diagram
- C3 with no stated boundary (pure library vs web, sync vs worker)
- Class/package dump as "C4 level 4"
- Diagrams that contradict an Accepted ADR
- Terms that are not in `CONTEXT.md`
