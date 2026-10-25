# ADR template

Copy the skeleton; do not copy the example's product content into another repo.

## Skeleton

```markdown
# ADR NNNN: <short title>

**Status:** Accepted
**Date:** 5 June 2026
**Decision context:** repository structure, module boundaries

## 1. Context

The product core is <X>. It is the most complex part. At the same time we need <Y>.
The temptation is to <couple A into B>.

Problems with that coupling:
1. …
2. …
3. …

## 2. Decision

Extract <X> into <package> with hard boundaries:

1. **Rule one.** …
2. **Named object** — the single thing that flows through every step.
3. **Interface for phase 1** — how it runs without the rest of the system.
4. Related decisions live in [ADR NNNN](NNNN-slug.md); do not repeat them here.

## 3. Consequences

### Positive
- …
- …

### Negative and risks
- <duplication / extra seam>. *Mitigation:* …
- <temptation to cut corners>. *Mitigation:* rule in CLAUDE.md / review grep.
```

## Filled structural example (trimmed)

```markdown
# ADR 0001: Pricing engine — pure library, isolated from web and DB

**Status:** Accepted
**Date:** 5 June 2026
**Decision context:** repository structure, module boundaries

## 1. Context

The product core is the pricing engine: discounts, taxes, and shipping rules
change every week. At the same time we need a web shop and a database. The
temptation is to compute prices directly in FastAPI routes, calling ORM models.

Problems with that coupling:
1. You cannot price a cart without a running web stack and DB.
2. Pricing unit tests pull in backend/app/DB/sessions.
3. Tax-provider calls spread across the codebase; retries and logging diverge.

## 2. Decision

Extract pricing into `backend/core/` as a **pure library**:

1. **Zero imports from `backend/app/`.** Input — a `Cart` + `PricingContext`;
   output — `list[PriceLine]`. Only the application service connects core and app.
2. **`PricingContext`** — the single object flowing through every rule.
3. **CLI as the phase-1 interface** — price a sample cart from the terminal, no web layer.
4. **Single tax-provider entry point** — see ADR 0002; never import the vendor SDK in app code.

## 3. Consequences

### Positive
- Pricing is developed from the CLI throughout phase 1.
- Pricing tests mock one client, not the web stack.
- The engine is portable: regression tests, CLI, and the web shop share code.

### Negative and risks
- Contract duplication: pydantic `PriceLine` vs ORM `OrderLineRow`.
  *Mitigation:* fields mirror one-to-one; conversion in one place, covered by a test.
- Temptation to import a DB session into a pricing rule.
  *Mitigation:* rule in CLAUDE.md; review greps `from app` under `backend/core/`.
```

## Optional extras (only if they earn the load)

```markdown
## Alternatives considered

### Option A: <name>
**Why rejected:** …
**When it would have been right:** …
```

Status line when replacing a past decision:

```markdown
**Status:** Accepted
**Supersedes:** [ADR 0008](0008-old-slug.md)
```

And on the old file:

```markdown
**Status:** Superseded by [ADR 0031](0031-new-slug.md)
```
