---
name: eli5
description: Explain a topic like I'm a 5 year old. Use when the user types /eli5 or asks for a dead-simple picture explainer of how something works.
argument-hint: "the topic to explain"
---

# eli5

Explain the topic like someone who knows nothing about it. The deliverable is a self-contained HTML page with **big pictures and very few words** — a picture book, not an essay.

Topic: the subject in the user's message (after `/eli5` or `eli5` if they named one). If they only invoked the skill, ask once.

## Output

Write one HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows). Write `<tmpdir>/eli5-<slug>-<timestamp>.html`. Open it — `xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows — and tell them the absolute path.

The page:

- Huge illustrations (inline SVG, CSS shapes, or oversized emoji). Pictures carry the meaning.
- Short captions. A few words per beat. No jargon paragraphs.
- One idea per section. Scroll is a story: setup → the thing happening → why it matters.
- Self-contained: inline CSS, no build, no CDN required.

Do not put the explainer in chat. One sentence: what you made and where it is.
