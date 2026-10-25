# Architecture

System documentation: **why** (ADR), **what** (C4), **how well** (quality scenarios), **skeleton** (arc42). Not about deepening modules in code — that is `engineering/codebase-design`.

The documents: `CONTEXT.md`, `docs/C4.md` (Mermaid), `adr/NNNN-slug.md`, plus an [arc42](https://arc42.org/) spine in `docs/arc42.md`.

## Skills

**Model-invoked**

- **[adr-write](./adr-write/SKILL.md)** — write or supersede an ADR in Context / Decision / Consequences form
- **[c4-diagrams](./c4-diagrams/SKILL.md)** — C1–C3, ERD instead of code-level C4, pipeline and sequence in Mermaid
- **[quality-scenarios](./quality-scenarios/SKILL.md)** — NFRs as measurable scenarios (ISO 25010 + SEI)
- **[threat-model](./threat-model/SKILL.md)** — STRIDE on flows from C4, trust boundaries
- **[architecture-styles](./architecture-styles/SKILL.md)** — monolith / hexagonal / services / events → ADR
- **[system-design](./system-design/SKILL.md)** — write the arc42 spine (`docs/arc42.md`)
- **[archify](./archify/SKILL.md)** — interactive HTML diagrams (architecture, workflow, sequence, dataflow, lifecycle) from JSON or Mermaid; needs Node ≥ 18 ([tt-a1i/archify](https://github.com/tt-a1i/archify), MIT)

**User-invoked**

- **[arc42-c4](./arc42-c4/SKILL.md)** — fill in the full pack and keep diagrams in sync with ADRs
- **[architecture-review](./architecture-review/SKILL.md)** — mini-ATAM: sensitivity, trade-off, risk
- **[architecture-lint](./architecture-lint/SKILL.md)** — read-only: ADR form, terms, C4↔ADR links

## How they connect

`system-design` writes the spine. `arc42-c4` orchestrates the pack. Sections 3/5/6/7 are drawn by `c4-diagrams`. Section 9 is written by `adr-write`. Section 10 is `quality-scenarios`. Section 12 is `CONTEXT.md`. System style is chosen by `architecture-styles`. Risks: `architecture-review` (quality) and `threat-model` (security). Before handoff — `architecture-lint`.
