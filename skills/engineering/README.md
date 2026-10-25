# Engineering

Generic engineering skills: module design, review, research, patterns. Not stack-specific (LangGraph, LLM infra, Spec Kit) — those live under `stacks/` and `speckit/`.

Source for several of these: [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering) (MIT). See [NOTICE.md](./NOTICE.md).

**Module design**

- **[wayfinder](./wayfinder/SKILL.md)** — plan an effort too big for one session as a map of decision tickets on the issue tracker; resolve one per session
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — `grill-me`, but immediately sharpens `CONTEXT.md` and ADRs
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** — codebase survey: shallow modules → HTML report → grilling of the chosen one
- **[domain-modeling](./domain-modeling/SKILL.md)** — living glossary in `CONTEXT.md` and ADRs only for real trade-offs
- **[codebase-design](./codebase-design/SKILL.md)** — vocabulary of deep modules: interface, seam, adapter, testability

**Review and research**

- **[research](./research/SKILL.md)** — research a question from primary sources and save citable Markdown
- **[spike](./spike/SKILL.md)** — plan how to check a claim; run in `.scratch/` only if asked; log keep / kill / unknown
- **[code-review](./code-review/SKILL.md)** — review a diff from a fixed viewpoint along two axes: Standards and Spec

**Spec → tickets → code**

- **[to-spec](./to-spec/SKILL.md)** — turn the current conversation into a spec (user stories, decisions, seams) and publish it to the tracker; no interview
- **[to-tickets](./to-tickets/SKILL.md)** — split a spec into tracer-bullet tickets with blocking edges; expand–contract for wide refactors
- **[triage](./triage/SKILL.md)** — move issues/PRs through `needs-triage` → `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`; write agent briefs
- **[implement](./implement/SKILL.md)** — build from a spec or tickets: tdd at agreed seams, typecheck, tests, then code-review
- **[tdd](./tdd/SKILL.md)** — red → green at pre-agreed seams; mocking and test-quality references
- **[prototype](./prototype/SKILL.md)** — throwaway prototype to answer a design question: logic (single HTML state-machine demo) or UI (variants on one route)

**Debugging and ops**

- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — diagnosis loop for hard bugs and perf regressions; HITL reproduce script
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — resolve an in-progress merge/rebase from primary sources; never `--abort`
- **[wizard](./wizard/SKILL.md)** — generate an interactive bash wizard for steps only a human can do (credentials, dashboards, one-off migrations)

**Patterns and style**

- **[clean-code](./clean-code/SKILL.md)** — naming, function shape, comments, error handling, code smells
- **[python-code-style](./python-code-style/SKILL.md)** — 21 binding Python rules: Pydantic, Sphinx docstrings, Ruff, naming, exceptions, logging, async, tests, imports, immutability, layering
- **[dependency-injection](./dependency-injection/SKILL.md)** — constructor injection against `Protocol`s, FastAPI `Depends()` as the DI mechanism, one composition root, testing with injected fakes
- **[api-design-patterns](./api-design-patterns/SKILL.md)** — API contracts, pagination, errors
- **[design-patterns](./design-patterns/SKILL.md)** — Singleton or Factory for service-backend infrastructure
- **[singleton-pattern](./singleton-pattern/SKILL.md)** — process-wide singletons for clients and services: explicit init, lazy, `@lru_cache`
- **[factory-pattern](./factory-pattern/SKILL.md)** — `XxxFactory` that builds and holds services or compiled graphs, bridged to FastAPI `Depends`

**GoF patterns** (`patterns/`, generic, not project-specific)

- **[design-patterns-catalog](./patterns/design-patterns-catalog/SKILL.md)** — index: which GoF pattern fits a problem, links to each pattern's own skill below

*Creational* — [factory-method-pattern](./patterns/factory-method-pattern/SKILL.md) · [abstract-factory-pattern](./patterns/abstract-factory-pattern/SKILL.md) · [builder-pattern](./patterns/builder-pattern/SKILL.md) · [prototype-pattern](./patterns/prototype-pattern/SKILL.md)

*Structural* — [adapter-pattern](./patterns/adapter-pattern/SKILL.md) · [decorator-pattern](./patterns/decorator-pattern/SKILL.md) · [facade-pattern](./patterns/facade-pattern/SKILL.md) · [composite-pattern](./patterns/composite-pattern/SKILL.md) · [proxy-pattern](./patterns/proxy-pattern/SKILL.md) · [bridge-pattern](./patterns/bridge-pattern/SKILL.md)

*Behavioral* — [strategy-pattern](./patterns/strategy-pattern/SKILL.md) · [observer-pattern](./patterns/observer-pattern/SKILL.md) · [command-pattern](./patterns/command-pattern/SKILL.md) · [state-pattern](./patterns/state-pattern/SKILL.md) · [template-method-pattern](./patterns/template-method-pattern/SKILL.md) · [chain-of-responsibility-pattern](./patterns/chain-of-responsibility-pattern/SKILL.md) · [mediator-pattern](./patterns/mediator-pattern/SKILL.md) · [iterator-pattern](./patterns/iterator-pattern/SKILL.md) · [visitor-pattern](./patterns/visitor-pattern/SKILL.md) · [memento-pattern](./patterns/memento-pattern/SKILL.md)
