---
name: architecture-review
description: >-
  Evaluate an existing architecture against quality scenarios: mini-ATAM with
  utility tree, sensitivity points, trade-offs, and risks. Use when the user
  asks to review architecture, assess a design, run ATAM, find architectural
  risks, or whether the C4/ADR pack is sound.
disable-model-invocation: true
---

# Architecture review

Ask: given **these** quality scenarios, how well does **this** design serve them, and where serving one hurts another?

Lightweight [ATAM](https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/) (SEI/CMU) — not a multi-day workshop. Review **artefacts** (C4, ADRs, quality.md), not taste.

Inputs: [c4-diagrams](../c4-diagrams/SKILL.md), [adr-write](../adr-write/SKILL.md), [quality-scenarios](../quality-scenarios/SKILL.md). If `docs/quality.md` is missing, draft scenarios first (or `TODO:` and stop).

## Process

1. **Drivers** — one paragraph: who the system is for, what must not fail.
2. **Approaches** — list the architectural moves actually present (pure library, async worker, single origin, …) with ADR links. Do not invent moves the docs do not show.
3. **Utility tree** — take or write the top (H,H) and (H,M) scenarios.
4. **Analyze** each high-priority scenario:
   - which container/approach addresses it
   - **Sensitivity** — a decision that strongly moves *one* attribute
   - **Trade-off** — a decision that helps one attribute and hurts another
   - **Risk** — a decision or *omission* that may fail the scenario under realistic load
   - **Non-risk** — analyzed and adequate given stated priorities
5. **Risk themes** — group risks (not a flat laundry list).
6. **Verdict** — `Approved` / `Approved with changes` / `Needs revision`. Each finding: evidence (file + diagram/ADR id) + concrete remediation (often "write ADR N" or "add trust boundary to C2").

Do not merge findings into a single "score". Axes stay separate.

## Output

Write `docs/architecture-review.md` (or print in chat if the user said not to save).

```markdown
# Architecture review — <date>

**Verdict:** Approved with changes
**Scope:** docs/C4.md + adr/ + docs/quality.md

## Drivers
…

## Approaches in play
- ADR 0001 — pricing engine as pure library
- ADR 0003 — async worker for payment webhooks

## Scenario analyses

### Q-01 (H,H) — tax-provider outage must not block checkout
- Approach: cached tax rates + fallback (ADR 0002)
- Sensitivity: retry/timeout policy on TaxClient
- Trade-off: tax accuracy vs checkout latency
- Finding: Non-risk for MVP; Risk if TaxClient retries unbounded
- Remediation: cap retries (already in ADR 0002) — confirm it is in C3

## Risk themes
1. Duplicate charges if payment webhooks are retried without idempotency — ADR 0007
2. …

## Actions
- [ ] …
```

## What this is not

- Not `code-review` (diff vs standards/spec)
- Not `improve-codebase-architecture` (deepen shallow modules)
- Not a security audit — for STRIDE use [threat-model](../threat-model/SKILL.md)
