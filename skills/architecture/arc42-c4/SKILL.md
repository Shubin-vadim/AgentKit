---
name: arc42-c4
description: Fill arc42 architecture documentation and keep C4 diagrams plus ADRs in sync. Use when the user asks for arc42, architecture documentation, a docs/C4.md pack, onboarding docs for how the system works, or a full architecture spec repo.
disable-model-invocation: true
---

# arc42 + C4

arc42 is the **12-section template** for architecture documentation. C4 is the **diagram model** that fills the structural sections. ADRs are the **why**.

This skill orchestrates. For the prose spine, read and follow [system-design](../system-design/SKILL.md). For diagrams, read and follow [c4-diagrams](../c4-diagrams/SKILL.md). For decisions, read and follow [adr-write](../adr-write/SKILL.md). For measurable NFRs, read and follow [quality-scenarios](../quality-scenarios/SKILL.md). After a full pack exists, [architecture-review](../architecture-review/SKILL.md) and [architecture-lint](../architecture-lint/SKILL.md) check it.

Do not use a full arc42 pack for a toy repo (under ~10 source files) — a README is enough.

## Target layout (prefer this)

Use this layout unless the repo already has another tree:

```text
CONTEXT.md                 # §12 glossary — binding language
docs/C4.md                 # §3, §5, §6, §7 diagrams (Mermaid)
adr/NNNN-slug.md           # §9 decisions
docs/arc42.md              # spine — remaining prose, pointers (skill `system-design`)
README.md                  # reading order + ADR index
```

A single giant `docs/architecture/arc42.md` is acceptable only when the user asks for one file. Prefer split docs that stay short.

If generating from **source**, document only what the code supports. Leave `TODO:` where only a human knows (quality goals, named stakeholders). Do not invent ADRs for guessed history.

## Section map

| # | arc42 | Where it lives | Diagram / skill |
|---|--------|----------------|-----------------|
| 1 | Introduction & Goals | `docs/arc42.md` | [system-design](../system-design/SKILL.md) |
| 2 | Constraints | prose; hard ones become ADRs | [adr-write](../adr-write/SKILL.md) |
| 3 | Context & Scope | `docs/C4.md` C1 | [c4-diagrams](../c4-diagrams/SKILL.md) |
| 4 | Solution Strategy | short prose + pointers to ADRs | system-design, adr-write |
| 5 | Building Block View | `docs/C4.md` C2 + C3 | c4-diagrams |
| 6 | Runtime View | sequence + pipeline in `docs/C4.md` | c4-diagrams |
| 7 | Deployment View | C2 host subgraph / deploy notes | c4-diagrams |
| 8 | Cross-cutting Concepts | only concepts the system actually has | system-design |
| 9 | Architecture Decisions | `adr/` + index in README | adr-write |
| 10 | Quality Requirements | `docs/quality.md` | [quality-scenarios](../quality-scenarios/SKILL.md) |
| 11 | Risks & Technical Debt | review + threat model | [architecture-review](../architecture-review/SKILL.md), [threat-model](../threat-model/SKILL.md) |
| 12 | Glossary | `CONTEXT.md` | same `_Avoid_:` style as domain glossary |

Always produce **1, 3, 5, 9, 12** when the user asked for architecture docs. Add 6/7/8 when there is a real runtime, deploy, or cross-cutting pattern. Skip empty sections rather than pad.

## Workflow

1. Read `CONTEXT.md`, existing `adr/`, `docs/C4.md`, and (if any) `TASK.md` / PRD.
2. Confirm layout with the user only if both `adr/` and `docs/adr/` exist.
3. Fill C1 → C2 → C3 via `c4-diagrams`. Stop at the first level that would be fiction.
4. For each hard choice that is not already an ADR, write one via `adr-write` (or list `TODO:` candidates — do not fabricate rationale).
5. Write remaining arc42 prose via `system-design` as pointers into those files, not a second copy of the diagrams.
6. Update README reading order.

## Maintenance

| Change | Update |
|--------|--------|
| New external system | C1, §3 |
| New container / store | C2, §5, maybe §7 |
| New module boundary | C3 + ADR |
| New Accepted ADR | §9 index, affected C4 figure |
| New glossary term | `CONTEXT.md` first, then diagrams |

## Anti-patterns

- Building-block section with no diagram
- ADRs only inlined in §9 and not as `adr/*.md` files
- PlantUML when the repo's C4 is Mermaid
- Stale docs after a structural ADR — worse than none
- Relitigating an Accepted ADR in prose instead of superseding it
