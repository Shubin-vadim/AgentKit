---
name: clean-code
description: >-
  Language-agnostic clean-code principles: naming, function size and shape,
  comments, formatting, error handling, and common code smells. Use when
  writing or reviewing code for readability, when the user asks for a
  clean-code pass, or when style feels off but there's no linter rule for it.
  Complements `codebase-design` (module/interface level) — this is
  statement/function/file level.
---

# Clean Code

Code is read far more often than it's written. Optimize for the next reader (often you, in six months, with no memory of today's context). None of this is about taste for its own sake — every rule below exists to cut the time it takes someone to build a correct mental model of what the code does.

Apply as judgment, not as a checklist to satisfy mechanically — a rule that makes a specific piece of code harder to follow loses to readability every time.

## Naming

- Name reveals intent: `elapsedTimeInDays` beats `d`; a reader shouldn't need to open the function body to know what a variable holds.
- Pick one word per concept project-wide (`fetch` xor `get` xor `retrieve` — not all three for the same operation across the codebase).
- Avoid disinformation: don't call something `accountList` if it's not actually a list; don't name near-identical concepts `data` vs `theData`.
- Length should match scope: `i` is fine in a 3-line loop; a module-level variable earns a full name.
- Booleans read as predicates: `isValid`, `hasPermission`, not `valid`, `flag`, `check`.
- Avoid encodings that fight the language/tooling (Hungarian notation, `m_` prefixes) — the type checker and IDE already carry that information.

## Functions

- Do one thing, at one level of abstraction. If you can extract a chunk and give it a name that isn't just a restatement of the code, it's doing more than one thing.
- Small: a function you can read without scrolling is a function whose whole behavior fits in working memory.
- Few arguments: 0–2 is comfortable, 3 needs justification, 4+ usually wants a parameter object. Boolean flag arguments (`render(fast=True)`) are a signal the function actually does two things — split it.
- No hidden side effects: a function named `checkPassword` that also starts a session is lying to its callers.
- Command-query separation: a function either does something (command) or answers something (query), not both — `pop()` doing both is a well-known wart, not a model to copy.
- Extract until the name is more informative than the body would be at a glance — but stop before you're extracting one-line wrappers that add navigation cost with no comprehension benefit.

## Comments

- Prefer a better name or an extracted function over a comment explaining what code does — comments explaining *what* rot the moment the code changes; the code should say what, the comment (if any) should say *why*.
- Good comment: a non-obvious constraint, a workaround for a specific bug/library quirk, a warning about a subtle consequence of changing this. Bad comment: restating the next line, a commented-out block "just in case," a changelog entry embedded in code.
- Delete comments that no longer match the code instead of leaving them stale — a wrong comment is worse than no comment.

## Formatting and structure

- Consistent formatting throughout a file/project — let an autoformatter own this so nobody argues about it in review.
- Vertical order mirrors reading order: high-level/entry-point code near the top, details it depends on below (newspaper style) — a reader shouldn't have to jump around to follow the main path.
- Related code stays close: a variable near its use, a helper near its caller, not scattered to "organize by type."
- Keep lines and files short enough to hold in view — a 2000-line file or a 300-character line is itself a readability bug, independent of what's in it.

## Error handling

- Fail fast and loud at the boundary where invalid state is detected; don't let bad data silently propagate deeper.
- Use exceptions/results for exceptional or absent cases, not as control flow for expected branches.
- Don't return `null`/`None`/sentinel values from a function whose callers will forget to check — prefer raising, an `Optional`/`Result` type, or a documented default.
- Catch only what you can meaningfully handle at that layer; a bare `except:`/`catch (e)` that swallows everything hides real bugs.
- Provide context in error messages (what operation, what input) — a caller debugging at 2am shouldn't have to reconstruct that from a stack trace alone.

## Common code smells to flag in review

- **Duplicated logic** (same conditional or calculation copy-pasted in 3 places) — extract once there's a real third occurrence, not preemptively at two.
- **Long parameter lists / data clumps** (the same 3 args always travel together) — bundle into a type.
- **Feature envy** (a method that mostly reaches into another object's internals) — it probably belongs on that other object.
- **Shotgun surgery** (one conceptual change requires edits across many unrelated files) — usually means the concept isn't actually encapsulated anywhere.
- **Dead code** (unused branches, commented-out blocks, unreachable `except`) — delete it; version control remembers it, the reader shouldn't have to.
- **Magic numbers/strings** — name them as constants when the value has meaning beyond its literal use.
- **Deep nesting** (4+ levels of `if`/loop) — invert conditions, extract guard clauses, or extract a function to flatten it.

## When not to apply these rules

- Throwaway scripts and prototypes meant to be deleted — see `prototype`.
- Code the team's linter/formatter already enforces mechanically — don't relitigate what the tool settles.
- A codebase with an established, different local convention — match it over these defaults; consistency within a file beats an abstract ideal.

## Related

- `codebase-design` — module/interface-level vocabulary (depth, seams, adapters), one level up from this file/function-level guidance
- `design-patterns-catalog` — when a code smell (duplicated variants, tangled conditionals) actually points at a specific pattern
- `code-review` — using these smells as part of a structured review pass
