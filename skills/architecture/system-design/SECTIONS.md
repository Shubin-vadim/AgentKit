# arc42 sections

Section names follow the [arc42](https://arc42.org/) template ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)). Fill the spine `docs/arc42.md`. Point at diagrams, ADRs, and the glossary — do not duplicate them.

| # | Section | Lives in | Write here |
|---|---------|----------|------------|
| 1 | Introduction and Goals | spine | what the system is, 3–5 quality goals, stakeholders |
| 2 | Architecture Constraints | spine; hard ones → ADR | tables: technical / organizational / conventions |
| 3 | Context and Scope | C1 in `docs/C4.md` | partner table + pointer to C1 |
| 4 | Solution Strategy | spine + ADR links | short list of approaches, each linked to an ADR |
| 5 | Building Block View | C2/C3 in `docs/C4.md` | pointer + one-line responsibility per container |
| 6 | Runtime View | sequence/pipeline in `docs/C4.md` | pointer to the key path only |
| 7 | Deployment View | deploy notes in `docs/C4.md` | where processes run, what they need |
| 8 | Cross-cutting Concepts | spine | only patterns the system actually has |
| 9 | Architecture Decisions | `adr/` | index with status; bodies stay in files |
| 10 | Quality Requirements | `docs/quality.md` | pointer; scenarios not slogans |
| 11 | Risks and Technical Debt | spine | named risk + mitigation; or threat-model pointer |
| 12 | Glossary | `CONTEXT.md` | pointer; do not fork a second glossary |

## 1. Introduction and Goals

Three blocks:

- **Requirements overview** — one short paragraph plus a link to the spec (`docs/agents/issue-tracker.md`, PRD, Tracker). Version the link if the spec moves.
- **Quality goals** — 3–5 rows: priority, ISO 25010 characteristic, one scenario. Measures from [quality-scenarios](../quality-scenarios/SKILL.md). No invented numbers.
- **Stakeholders** — role, what they need from this document. Names and emails only if the user supplied them.

## 2. Architecture Constraints

Tables, not essays. Split: technical (cloud, language, must-use systems), organizational (team, compliance), conventions (repo layout, docs). A constraint that hides a trade-off becomes an ADR via [adr-write](../adr-write/SKILL.md).

Skip when there are no real constraints yet.

## 3. Context and Scope

Pointer to **C1** in `docs/C4.md`. Add a table: communication partner, in, out. Scope-out list (what this system is *not*). Business vs technical context: one table each if they differ; otherwise one table.

## 4. Solution Strategy

Five to ten bullets: style ([architecture-styles](../architecture-styles/SKILL.md)), sync vs async, where state lives, how you slice modules. Each bullet that is hard to reverse links an ADR. This section is the map, not the argument — the argument is the ADR.

## 5. Building Block View

Pointer to **C2** (and **C3** only if a module boundary exists). Table: building block, responsibility, owner if known. Level 1 = the system as one box (already C1). Level 2 = containers. Do not dump packages or classes.

## 6. Runtime View

Pointer to the **sequence** or **pipeline** of the one path that matters (the user journey or the job). Extra scenarios only when they change the design. Skip if the system has no interesting runtime yet.

## 7. Deployment View

Pointer to the host subgraph / deploy notes in `docs/C4.md`. What runs where, how many instances, which store is durable. Skip for a single local process with no deploy.

## 8. Cross-cutting Concepts

One heading per concept the code actually uses: auth, domain events, transactional outbox, multi-tenancy, i18n, observability. A paragraph + pointer to the module or ADR. Skip concepts you might use later.

## 9. Architecture Decisions

Index table: number, title, status, one-line effect. Link to `adr/NNNN-slug.md`. Do not paste Context/Decision/Consequences into the spine.

## 10. Quality Requirements

Pointer to `docs/quality.md`. If that file does not exist and quality goals in §1 have no measures, write `TODO:` and stop — do not invent SLOs.

## 11. Risks and Technical Debt

Table: risk or debt, impact, mitigation or "accepted". Security flows: pointer to [threat-model](../threat-model/SKILL.md) when that file exists. Skip if nothing is known; do not invent a risk register.

## 12. Glossary

Pointer to `CONTEXT.md`. New terms go there first, then into diagrams and this document.
