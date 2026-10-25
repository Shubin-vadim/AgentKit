---
name: adr-write
description: >-
  Write or supersede Architecture Decision Records in a three-part shape:
  Context, Decision, Consequences. Use when the user asks for an ADR, records
  a hard-to-reverse architectural choice, or mentions adr/, docs/adr/,
  architecture decision, or superseding a past decision.
---

# ADR write

Record **why** a choice was made, not the implementation. Shape: numbered `NNNN-slug.md`, three sections, terms from `CONTEXT.md`.

Full template and a filled example: [ADR-TEMPLATE.md](ADR-TEMPLATE.md). If the project has `adr/_template.md` (installed with the `architecture` profile), start each new ADR from that file, and do not number or index the template itself.

## Where files live

Match the repo if ADRs already exist. Otherwise prefer `adr/` at the repo root. Accept `docs/adr/` if that is already the convention.

Filename: `NNNN-slug.md` — four-digit number, kebab-case slug, never reuse a number. Heading: `# ADR NNNN: <title>`.

After writing, add one line to the architecture README (or `adr/` index) and cross-link from `docs/C4.md` / arc42 section 9 when the decision changes structure.

## When to write

Write when **all three** hold:

1. **Hard to reverse** — swapping later is expensive (stack, module boundary, async vs sync, storage).
2. **Real trade-off** — at least two reasonable options existed.
3. **Surprising without context** — a future reader would otherwise "fix" it.

Do **not** write for function names, trivially reversible picks, or anything already covered by team standards.

## Workflow

1. Read `CONTEXT.md` (and existing `adr/` / `docs/adr/`). Reuse canonical terms; do not invent synonyms.
2. If the user has not named alternatives, ask for them in one round. Do not invent a fake "Option B".
3. Scan for the highest `NNNN` and increment.
4. Write a **new** file. Never rewrite an Accepted ADR in place. To change a decision: new ADR with **Status: Accepted**, old ADR **Status: Superseded by ADR NNNN**, and a link both ways.
5. Link related ADRs from the Decision or Consequences, not a dump of the whole catalog.

## Status

`Draft` → `Proposed` → `Accepted` → `Deprecated` | `Superseded by ADR NNNN`

Default new records to `Accepted` only when the user has chosen. Otherwise `Draft` or `Proposed`.

## Shape (required)

```markdown
# ADR NNNN: <short title>

**Status:** Draft | Proposed | Accepted | Deprecated | Superseded by ADR NNNN
**Date:** <day Month YYYY>
**Decision context:** <one-line scope: module boundaries, stack, pipeline, …>
```

Then numbered sections:

1. **Context** — situation, constraints, what goes wrong if we couple the wrong way. Specific, not background essays.
2. **Decision** — numbered hard rules the implementation must follow. Link sibling ADRs instead of repeating them.
3. **Consequences** — `### Positive` and `### Negative and risks`. Every negative names a *Mitigation* when there is one.

Optional **Alternatives considered** only when rejected options would otherwise be re-proposed in six months. Honest "why rejected" + "when it would have been right".

## Anti-patterns

- "We chose X because it's better" — say better *for this constraint*.
- Editing history of an Accepted ADR instead of superseding.
- ADR for a reversible detail.
- Terms that contradict `CONTEXT.md`.
- Empty Consequences or only positives.

## Checklist

- [ ] Filename `NNNN-slug.md`, heading matches the number
- [ ] Status + Date + Decision context
- [ ] Context names the coupling or constraint that forced the choice
- [ ] Decision is a list of enforceable rules, not a vibe
- [ ] Positive **and** negative consequences
- [ ] `CONTEXT.md` terms used exactly
- [ ] Index / README updated
- [ ] If superseding: old ADR status updated
