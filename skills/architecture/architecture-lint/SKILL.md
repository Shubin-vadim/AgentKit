---
name: architecture-lint
description: >-
  Read-only consistency check of architecture docs: ADR shape, C4 vs CONTEXT.md
  terms, ADR links, quality scenarios with measures. Use when the user asks to
  lint ADRs, check architecture docs, or whether C4/adr/glossary are in sync.
disable-model-invocation: true
---

# Architecture lint

Read-only. Report pass/fail with file:line. Do not rewrite docs unless the user asks after the report.

Scope: `CONTEXT.md`, `docs/C4.md`, `docs/arc42.md`, `adr/` or `docs/adr/`, `docs/quality.md`, `docs/threat-model.md`, README ADR index — whichever exists. A file that still has `<...>` placeholders is an unfilled template: report it once as "not filled" and skip its other gates. Ignore `adr/_template.md`.

## Gates

### 1. ADR completeness

For each `NNNN-slug.md`:

- Heading `# ADR NNNN:` matches filename number
- **Status**, **Date**, **Decision context** present
- `## 1. Context`, `## 2. Decision`, `## 3. Consequences` with non-empty bodies
- Consequences include a negative or risk (not only positives)
- Status is one of: Draft, Proposed, Accepted, Deprecated, `Superseded by ADR NNNN`
- Accepted ADRs are not silently rewritten in place: if two files share a number, fail
- Supersedes links: old file says Superseded, new file points back

Do **not** require MADR extras (Deciders, seven sections, Alternatives) unless the file already uses them.

### 2. Glossary

- Diagram labels and ADR titles use `CONTEXT.md` terms
- Avoid-list synonyms (`purchase` when the term is `Order`) fail this gate
- New boxes in C1 that are not in the glossary → fail or `TODO` in CONTEXT.md

### 3. C4 hygiene

- `docs/C4.md` has C1 and C2; C3 only if a boundary ADR exists
- Libraries are not C1 systems
- Each diagram has an *Audience:* line
- Accepted structural ADRs are linked from the diagram they constrain
- C2 containers that persist data have a store on the diagram

### 4. Quality

If `docs/quality.md` exists: each scenario has a **response measure**. Priority list is ≤ 5 attributes.

### 5. Index

README (or `adr/` index) lists every ADR number. Missing or extra numbers fail.

### 6. arc42 spine

If `docs/arc42.md` exists:

- Headings for §1, §3, §5, §9, §12 are present
- No fenced Mermaid that duplicates `docs/C4.md`
- §9 is an index of `adr/` files, not pasted ADR bodies
- §12 points at `CONTEXT.md` rather than a second glossary

## Output

```
Linting architecture docs

ADR completeness: FAIL
  adr/0004-stack-fastapi-react.md: Consequences has no negative (line 40)

Glossary: PASS

C4 hygiene: FAIL
  docs/C4.md: C1 includes SQLAlchemy as an external system (line 18)

Quality: PASS (no docs/quality.md — skipped)

Index: PASS

arc42 spine: PASS (no docs/arc42.md — skipped)

Next: fix C1 (drop the library), then add a negative to ADR 0004.
```

Zero FAIL → say so. Do not invent work.
