# OpenSpec

[OpenSpec](https://github.com/Fission-AI/OpenSpec) spec-driven workflow. **Always in `core`.** Feature TZ / change from a short description goes here, not into a free-form doc.

Official skills drive the `openspec` CLI. First time in a project: `openspec-init` (`npx @fission-ai/openspec init --tools none`) so kit skills in the client's skills folder are not overwritten.

Default path: explore → propose → apply → archive. Cursor slash: `/opsx-propose` (same skill as `openspec-propose`).

- **[openspec-init](./openspec-init/SKILL.md)** — create `openspec/` without rewriting Cursor skills
- **[openspec-explore](./openspec-explore/SKILL.md)** — think through a fuzzy idea (no code)
- **[openspec-propose](./openspec-propose/SKILL.md)** — proposal, delta specs, design, tasks
- **[openspec-apply-change](./openspec-apply-change/SKILL.md)** — implement tasks
- **[openspec-update-change](./openspec-update-change/SKILL.md)** — revise artifacts
- **[openspec-sync-specs](./openspec-sync-specs/SKILL.md)** — merge deltas into main specs
- **[openspec-archive-change](./openspec-archive-change/SKILL.md)** — archive a finished change

Expanded OpenSpec commands (`new`, `continue`, `ff`, `verify`, …) stay upstream; run `openspec update` in a project if you need them.

Source: [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), MIT. See [NOTICE.md](./NOTICE.md).
