---
name: spike
description: >-
  Plan how to verify a hypothesis, then run it only if asked. Data optional.
  Throwaway work in .scratch/, one note in docs/hypotheses/, no OpenSpec. Use
  when the user says spike, hypothesis, ad-hoc, experiment, "just check
  whether", or asks how to check a claim.
argument-hint: "the claim to check"
---

# Spike

Make the claim **checkable**, then prove or kill it only when asked. This is not a feature and not architecture work.

If `docs/hypotheses/` is missing, create it from the templates in the repo (or copy `_template.md`).

## Workflow

1. **Claim.** One sentence. **Falsify:** one observation that kills it. If either is missing, ask once. Do not invent a metric.

2. **Data.** Inventory what they attached or named (path, grain, fields). List what is missing. Do not invent a dataset.
   - **Present** — the method uses that data. Name the file/table/column.
   - **Absent** — the method says how to obtain evidence: source, grain, how much is enough, what would still leave **unknown**.

3. **Write the note.** Copy `docs/hypotheses/_template.md` to `docs/hypotheses/YYYY-MM-DD-slug.md`. Fill Claim, Falsify, Data, Method, Decide. Leave Did / Result / Throw away empty. Done with the plan when keep / kill / unknown each have a concrete observation and every missing input is named.

4. **Run only if they said** run, spike, or run it, **and** the method can run now (data in hand, or a throwaway code check that needs no external dataset). Time-box: one session if they gave no bound. Work only under `.scratch/`. Do not refactor production, do not add tests unless they asked, do not open an OpenSpec change. Then fill Did, Result (`keep` | `kill` | `unknown`), Throw away.

5. **Stop.** If Result is empty, stop at the plan. If **keep** and they want a product change, *offer* `openspec-propose` — do not start it in this run. Library facts: `research` or Context7; do not turn the spike into a research essay. `grill-me` only if the **claim** still has an open branch.

## Do not

- OpenSpec, ADR, arc42, C4, FastAPI scaffold, Spec Kit
- Production modules "while we're here"
- Fill empty data with made-up rows
