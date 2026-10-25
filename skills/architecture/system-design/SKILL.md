---
name: system-design
description: >-
  Write or update a system design document using the arc42 12-section template.
  Use when the user asks for a system design, architecture document, SAD,
  docs/arc42.md, or to document how the system is designed.
---

# System design (arc42)

Write **how the system is designed** as an [arc42](https://arc42.org/) document. arc42 is a 12-section skeleton for architecture communication — not a process and not a diagram language.

This skill writes the **spine**: `docs/arc42.md`. Diagrams, decisions, quality scenarios, and glossary stay in their files. What to put in each section: [SECTIONS.md](SECTIONS.md).

For C4 Mermaid, follow [c4-diagrams](../c4-diagrams/SKILL.md). For hard choices, [adr-write](../adr-write/SKILL.md). For measurable NFRs, [quality-scenarios](../quality-scenarios/SKILL.md). Style of the system: [architecture-styles](../architecture-styles/SKILL.md). After a full pack: [architecture-lint](../architecture-lint/SKILL.md).

Do not use a full arc42 pack for a toy repo (under ~10 source files) — a README is enough.

## Spine

```text
docs/arc42.md              # this skill — 12 sections, pointers not copies
docs/C4.md                 # §3, §5, §6, §7 diagrams
adr/NNNN-slug.md           # §9
docs/quality.md            # §10
CONTEXT.md                 # §12
```

One file `docs/arc42.md` is the default. Split only when a section outgrows a screen and the user agrees.

If generating from **source**, document only what the code supports. Leave `TODO:` where only a human knows (quality goals, named stakeholders). Do not invent ADRs for guessed history.

## Always produce

When the user asked for a system design: **§1, §3, §5, §9, §12**. Add §2/§4/§6/§7/§8/§10/§11 when there is a real constraint, strategy, runtime, deploy, cross-cutting concept, quality bar, or risk. Skip the rest with one line *why*, rather than padding.

## Workflow

1. Read `CONTEXT.md`, `docs/arc42.md`, `docs/C4.md`, `adr/`, `docs/quality.md` — whichever exist. A file that still has `<...>` placeholders is an unfilled template from the `architecture` profile: fill it in place and drop its HTML comments; do not treat placeholders as facts.
2. If the repo already has another architecture tree, fill that tree; do not start a second spine.
3. Fill C1 → C2 → C3 via `c4-diagrams`. Stop at the first level that would be fiction.
4. For each hard choice that is not already an ADR, write one via `adr-write` (or list `TODO:` candidates).
5. Write `docs/arc42.md` as **pointers** into those files plus the short tables in [SECTIONS.md](SECTIONS.md). Do not paste Mermaid or ADR bodies into the spine.
6. Point the architecture README (or repo README) at `docs/arc42.md` as the reading start.

## Anti-patterns

- Second copy of a C4 diagram inside §3/§5/§6/§7
- ADRs only inlined in §9 and not as `adr/*.md`
- Empty sections filled with lorem or "TBD" with no owner
- Relitigating an Accepted ADR in prose instead of superseding it
- Synonyms that are not in `CONTEXT.md`
