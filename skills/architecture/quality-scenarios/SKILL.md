---
name: quality-scenarios
description: >-
  Turn non-functional needs into measurable quality-attribute scenarios (ISO/IEC
  25010 + SEI six-part form). Use when the user asks for NFRs, quality goals,
  quality tree, arc42 section 10, SLOs, or "how well" the system must behave.
---

# Quality scenarios

Architecture is chosen against **quality attributes**, not features. Vague "must be fast and secure" is not a requirement. A scenario is.

Fills arc42 §1 quality goals and §10. Hard trade-offs that lock a design become ADRs via [adr-write](../adr-write/SKILL.md).

Vocabulary: [ISO/IEC 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) characteristics, [SEI quality-attribute scenarios](https://www.sei.cmu.edu/) (Bass / Clements / Kazman).

## When

- Starting architecture docs and §10 is empty
- Comparing two designs ("which is better?")
- Before an [architecture-review](../architecture-review/SKILL.md)
- User says NFR, SLO, latency, availability, threat, maintainability

Do not invent numbers. If the user has no measure, write `TODO:` and ask once.

## Pick attributes (few)

Name **3–5** priority characteristics for *this* system. Typical set from ISO 25010:

| Characteristic | Ask |
|----------------|-----|
| Performance efficiency | time, resources, capacity |
| Reliability | availability, fault tolerance, recoverability |
| Security | confidentiality, integrity, authenticity, non-repudiation |
| Maintainability | modifiability, testability, modularity |
| Compatibility | interoperability with named externals |
| Usability | only when the product *is* the UI |

Drop the rest. A utility tree with 12 top-level goals is unused.

## Scenario form (required)

One scenario = one testable sentence. Six parts:

| Part | Meaning |
|------|---------|
| **Source** | who/what stimulates (user, operator, failing node, attacker) |
| **Stimulus** | the event |
| **Environment** | normal / peak / degraded / startup |
| **Artifact** | which container or flow (use C4 names) |
| **Response** | what the system does |
| **Response measure** | number + unit + percentile or SLO |

Three kinds (label each):

- **Usage** — normal work
- **Growth** — change / load increase
- **Exploratory** — failure, abuse, boundary

## File

Write `docs/quality.md` (create `docs/` lazily) unless the repo already keeps this in `docs/arc42.md` §10. If the file still has `<...>` placeholders, it is the installed template: fill it in place and drop its HTML comments.

```markdown
# Quality requirements

Priority attributes: Reliability, Security, Performance efficiency, Maintainability.

## Utility tree

- Reliability
  - Q-01 (H,M) Checkout keeps working when the tax provider fails
  - Q-02 (H,H) Recover the payment worker after a crash mid-job
- Security
  - Q-03 (H,L) Customers see only their own orders

(H,M) = importance for stakeholders, difficulty to achieve.

## Scenarios

### Q-01 — Usage — Reliability
- Source: TaxClient
- Stimulus: tax provider returns 5xx
- Environment: normal production
- Artifact: API / PricingEngine
- Response: use cached tax rates, flag the order for review, complete checkout
- Measure: checkout succeeds in 100% of single-provider outages in integration tests
```

## Anti-patterns

- "The system shall be scalable" with no measure
- Copying all eight ISO characteristics
- Measures the team cannot observe (no metric, no log, no test)
- Scenarios that name code types instead of C4 containers
