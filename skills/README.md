# Skills

Library of agent skills. Each skill is a folder with `SKILL.md`. Catalogs group by purpose. Nested paths are for authors; a project receives a **flat** copy of selected folders.

| Catalog | Purpose |
|---------|--------|
| [architecture/](./architecture/) | ADR, C4, arc42, NFR, STRIDE, architecture review |
| [engineering/](./engineering/) | Module design, review, research, generic patterns |
| [reverse-engineering/](./reverse-engineering/) | Evidence-led inspection of authorized shipped artifacts and runtime behavior |
| [frontend/](./frontend/) | Distinctive production UI (not templated AI aesthetics) |
| [productivity/](./productivity/) | Plan interviews, handoff, teaching, documents for agents |
| [openspec/](./openspec/) | OpenSpec SDD (always in `core`) |
| [speckit/](./speckit/) | Spec Kit feature workflow (optional) |
| [stacks/](./stacks/) | Stack packs: LangGraph, llm-infra, vLLM, SGLang |

## How to invoke

Name the skill in chat (`grill-me`, `handoff`, `adr-write`) or point to its `SKILL.md`.

**User-invoked** skills (`disable-model-invocation: true`) run only on an explicit request. **Model-invoked** skills also run when the agent itself sees a matching task.

Do not symlink this whole tree into a client. `scripts/kit.py install` copies selected skill folders into the client's skills directory (`.cursor/skills/`, `.claude/skills/`, `.opencode/skills/`, or `.agents/skills/`) and converts selected rules. Agents working in this kit find `apply-kit` through [AGENTS.md](../AGENTS.md).

## Architecture

System documentation: ADRs, C4 in Mermaid, arc42 skeleton.

- **[adr-write](./architecture/adr-write/SKILL.md)** — Context / Decision / Consequences in `adr/NNNN-slug.md`
- **[c4-diagrams](./architecture/c4-diagrams/SKILL.md)** — C1–C3, ERD, pipeline, sequence
- **[quality-scenarios](./architecture/quality-scenarios/SKILL.md)** — measurable NFRs (ISO 25010 + SEI scenarios)
- **[architecture-styles](./architecture/architecture-styles/SKILL.md)** — monolith / hexagonal / services → ADR
- **[threat-model](./architecture/threat-model/SKILL.md)** — STRIDE on C4, trust boundaries
- **[system-design](./architecture/system-design/SKILL.md)** — arc42 spine (`docs/arc42.md`)
- **[arc42-c4](./architecture/arc42-c4/SKILL.md)** — fill in arc42 and link diagrams to ADRs
- **[architecture-review](./architecture/architecture-review/SKILL.md)** — mini-ATAM against quality scenarios
- **[archify](./architecture/archify/SKILL.md)** — interactive HTML diagrams (architecture, workflow, sequence, dataflow, lifecycle) from JSON/Mermaid
- **[architecture-lint](./architecture/architecture-lint/SKILL.md)** — check consistency of ADRs / C4 / glossary

## Engineering

Generic engineering, not a stack. Plus skills from [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering) (MIT).

**Module design**

- **[wayfinder](./engineering/wayfinder/SKILL.md)** — plan an effort too big for one session as a map of decision tickets on the issue tracker; resolve one per session
- **[grill-with-docs](./engineering/grill-with-docs/SKILL.md)** — `grill-me`, but immediately sharpens `CONTEXT.md` and ADRs
- **[improve-codebase-architecture](./engineering/improve-codebase-architecture/SKILL.md)** — codebase survey: shallow modules → HTML report → grilling of the chosen one
- **[domain-modeling](./engineering/domain-modeling/SKILL.md)** — living glossary in `CONTEXT.md` and ADRs only for real trade-offs
- **[codebase-design](./engineering/codebase-design/SKILL.md)** — vocabulary of deep modules: interface, seam, adapter, testability

**Review and research**

- **[research](./engineering/research/SKILL.md)** — research a question from primary sources and save citable Markdown
- **[spike](./engineering/spike/SKILL.md)** — plan how to check a claim; run in `.scratch/` only if asked; log keep / kill / unknown
- **[code-review](./engineering/code-review/SKILL.md)** — review a diff from a fixed viewpoint along two axes: Standards and Spec

**Spec → tickets → code**

- **[to-spec](./engineering/to-spec/SKILL.md)** — turn the current conversation into a spec (user stories, decisions, seams) and publish it to the tracker; no interview
- **[to-tickets](./engineering/to-tickets/SKILL.md)** — split a spec into tracer-bullet tickets with blocking edges; expand–contract for wide refactors
- **[triage](./engineering/triage/SKILL.md)** — move issues/PRs through `needs-triage` → `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`; write agent briefs
- **[implement](./engineering/implement/SKILL.md)** — build from a spec or tickets: tdd at agreed seams, typecheck, tests, then code-review
- **[tdd](./engineering/tdd/SKILL.md)** — red → green at pre-agreed seams; mocking and test-quality references
- **[prototype](./engineering/prototype/SKILL.md)** — throwaway prototype to answer a design question: logic (single HTML state-machine demo) or UI (variants on one route)

**Debugging and ops**

- **[diagnosing-bugs](./engineering/diagnosing-bugs/SKILL.md)** — diagnosis loop for hard bugs and perf regressions; HITL reproduce script
- **[resolving-merge-conflicts](./engineering/resolving-merge-conflicts/SKILL.md)** — resolve an in-progress merge/rebase from primary sources; never `--abort`
- **[wizard](./engineering/wizard/SKILL.md)** — generate an interactive bash wizard for steps only a human can do (credentials, dashboards, one-off migrations)

**Patterns and style**

- **[clean-code](./engineering/clean-code/SKILL.md)** — naming, function shape, comments, error handling, code smells
- **[python-code-style](./engineering/python-code-style/SKILL.md)** — 21 binding Python rules: Pydantic, Sphinx docstrings, Ruff, naming, exceptions, logging, async, tests, imports, immutability, layering
- **[dependency-injection](./engineering/dependency-injection/SKILL.md)** — constructor injection against `Protocol`s, FastAPI `Depends()` as the DI mechanism, one composition root, testing with injected fakes
- **[api-design-patterns](./engineering/api-design-patterns/SKILL.md)** — API contracts, pagination, errors
- **[design-patterns](./engineering/design-patterns/SKILL.md)** — Singleton or Factory for service-backend infrastructure
- **[singleton-pattern](./engineering/singleton-pattern/SKILL.md)** — process-wide singletons for clients and services: explicit init, lazy, `@lru_cache`
- **[factory-pattern](./engineering/factory-pattern/SKILL.md)** — `XxxFactory` that builds and holds services or compiled graphs, bridged to FastAPI `Depends`

**GoF patterns** (`engineering/patterns/`, generic, not project-specific)

- **[design-patterns-catalog](./engineering/patterns/design-patterns-catalog/SKILL.md)** — index: which GoF pattern fits a problem, links to each pattern's own skill below

*Creational* — [factory-method-pattern](./engineering/patterns/factory-method-pattern/SKILL.md) · [abstract-factory-pattern](./engineering/patterns/abstract-factory-pattern/SKILL.md) · [builder-pattern](./engineering/patterns/builder-pattern/SKILL.md) · [prototype-pattern](./engineering/patterns/prototype-pattern/SKILL.md)

*Structural* — [adapter-pattern](./engineering/patterns/adapter-pattern/SKILL.md) · [decorator-pattern](./engineering/patterns/decorator-pattern/SKILL.md) · [facade-pattern](./engineering/patterns/facade-pattern/SKILL.md) · [composite-pattern](./engineering/patterns/composite-pattern/SKILL.md) · [proxy-pattern](./engineering/patterns/proxy-pattern/SKILL.md) · [bridge-pattern](./engineering/patterns/bridge-pattern/SKILL.md)

*Behavioral* — [strategy-pattern](./engineering/patterns/strategy-pattern/SKILL.md) · [observer-pattern](./engineering/patterns/observer-pattern/SKILL.md) · [command-pattern](./engineering/patterns/command-pattern/SKILL.md) · [state-pattern](./engineering/patterns/state-pattern/SKILL.md) · [template-method-pattern](./engineering/patterns/template-method-pattern/SKILL.md) · [chain-of-responsibility-pattern](./engineering/patterns/chain-of-responsibility-pattern/SKILL.md) · [mediator-pattern](./engineering/patterns/mediator-pattern/SKILL.md) · [iterator-pattern](./engineering/patterns/iterator-pattern/SKILL.md) · [visitor-pattern](./engineering/patterns/visitor-pattern/SKILL.md) · [memento-pattern](./engineering/patterns/memento-pattern/SKILL.md)

## Frontend

- **[frontend-design](./frontend/frontend-design/SKILL.md)** — distinctive production UI: palette, type, layout; reject templated AI defaults

## OpenSpec

Always installed with `core`. [OpenSpec](https://github.com/Fission-AI/OpenSpec) SDD. Skills from upstream except `openspec-init`.

- **[openspec-init](./openspec/openspec-init/SKILL.md)** — `openspec/` tree (`init --tools none`)
- **[openspec-explore](./openspec/openspec-explore/SKILL.md)** — think through a fuzzy idea
- **[openspec-propose](./openspec/openspec-propose/SKILL.md)** — proposal, specs, design, tasks
- **[openspec-apply-change](./openspec/openspec-apply-change/SKILL.md)** — implement tasks
- **[openspec-update-change](./openspec/openspec-update-change/SKILL.md)** — revise artifacts
- **[openspec-sync-specs](./openspec/openspec-sync-specs/SKILL.md)** — merge deltas into main specs
- **[openspec-archive-change](./openspec/openspec-archive-change/SKILL.md)** — archive a finished change

## Spec Kit

- **[speckit-constitution](./speckit/speckit-constitution/SKILL.md)** — Spec Kit project constitution
- **[speckit-specify](./speckit/speckit-specify/SKILL.md)** — feature specification
- **[speckit-clarify](./speckit/speckit-clarify/SKILL.md)** — clarifying questions on the spec
- **[speckit-plan](./speckit/speckit-plan/SKILL.md)** — implementation plan
- **[speckit-tasks](./speckit/speckit-tasks/SKILL.md)** — `tasks.md` with dependencies
- **[speckit-analyze](./speckit/speckit-analyze/SKILL.md)** — consistency of spec / plan / tasks
- **[speckit-checklist](./speckit/speckit-checklist/SKILL.md)** — requirements checklist
- **[speckit-implement](./speckit/speckit-implement/SKILL.md)** — execute the plan from `tasks.md`
- **[speckit-taskstoissues](./speckit/speckit-taskstoissues/SKILL.md)** — tasks → GitHub issues

## Stacks

**LangGraph**

- **[langgraph-fundamentals](./stacks/langgraph/langgraph-fundamentals/SKILL.md)** — StateGraph, tools, checkpointer, streaming

**LLM infra**

- **[llm-infra](./stacks/llm-infra/SKILL.md)** — local Docker commands: Qdrant, Langfuse, MLflow, Postgres, Redis, Kafka, Ollama

**vLLM**

- **[vllm-gpu](./stacks/vllm/vllm-gpu/SKILL.md)** — blank NVIDIA GPU server: driver, Docker, toolkit, official `vllm/vllm-openai`

**SGLang**

- **[sglang-gpu](./stacks/sglang/sglang-gpu/SKILL.md)** — blank NVIDIA GPU server: official `lmsysorg/sglang`, API key `sk-local-`, port 30000

## Productivity

Shared workflow skills from [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity) (MIT), plus `eli5` from [claude-plugins-community](https://github.com/anthropics/claude-plugins-community/tree/main/eli5) and `caveman` from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/main/skills/caveman).

**User-invoked**

- **[grill-me](./productivity/grill-me/SKILL.md)** — interrogate a plan or design until every branch is closed
- **[handoff](./productivity/handoff/SKILL.md)** — compact the session into a document for the next agent
- **[teach](./productivity/teach/SKILL.md)** — teach a topic across several sessions, keeping state in the current directory
- **[to-questionnaire](./productivity/to-questionnaire/SKILL.md)** — a decision you cannot close yourself → a questionnaire for one person
- **[wait-what](./productivity/wait-what/SKILL.md)** — the last message didn't land: restate it more simply, in `CONTEXT.md` language

**Model-invoked**

- **[eli5](./productivity/eli5/SKILL.md)** — explain a topic like I'm 5: HTML picture book, big pictures, few words
- **[caveman](./productivity/caveman/SKILL.md)** — ultra-compressed replies: drop fluff, keep technical substance
- **[write-prompt](./productivity/write-prompt/SKILL.md)** — compose an LLM prompt in `<Role>` / `<Task>` / `<Instructions>` tags
- **[grilling](./productivity/grilling/SKILL.md)** — the interview primitive behind `grill-me`
- **[writing-for-agents](./productivity/writing-for-agents/SKILL.md)** — write skills, `AGENTS.md` / `CLAUDE.md`, and any document an agent will read
- **[apply-kit](./productivity/apply-kit/SKILL.md)** — pick profiles from a short description and install them for any client

## Sources

- Matt Pocock skills (`productivity/` and part of `engineering/`): [mattpocock/skills](https://github.com/mattpocock/skills), MIT License, Copyright (c) 2026 Matt Pocock
- `eli5`: [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community/tree/main/eli5), Thariq Shihipar (plugin MIT; repo Apache-2.0)
- `caveman`: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/main/skills/caveman), MIT
- `frontend-design`: [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design), Apache-2.0
- `reverse-engineer-anything`: [morluto/rea](https://github.com/morluto/rea), MIT
- OpenSpec skills (`openspec/`): [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), MIT
- Spec Kit skills: GitHub Spec Kit (`templates/commands`)
- Architecture: section template — [arc42](https://arc42.org); diagrams — [C4 model](https://c4model.com); evaluation — [ATAM](https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/); quality — [ISO/IEC 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010); threats — [STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
