# Templates

Portable project files that are not rules. Rules live in [rules/](../rules/).
Profiles list templates under `templates:` (`src` or `src => dest`). A client
adapter copies a file only if the destination does not already exist (`--force`
overwrites in the current Cursor adapter).

| File | Typical dest | Profile |
|------|----------------|---------|
| `AGENTS.md` | `AGENTS.md` | `core` |
| `CONTEXT.md` | `CONTEXT.md` | `core` |
| `docs/agents/issue-tracker.md` | `docs/agents/issue-tracker.md` | `core` |
| `architecture/docs/C4.md` | `docs/C4.md` | `architecture` |
| `architecture/docs/arc42.md` | `docs/arc42.md` | `architecture` |
| `architecture/docs/quality.md` | `docs/quality.md` | `architecture` |
| `architecture/docs/threat-model.md` | `docs/threat-model.md` | `architecture` |
| `architecture/adr/README.md` | `adr/README.md` | `architecture` |
| `architecture/adr/_template.md` | `adr/_template.md` | `architecture` |
| `docs/hypotheses/README.md` | `docs/hypotheses/README.md` | `spike` |
| `docs/hypotheses/_template.md` | `docs/hypotheses/_template.md` | `spike` |
| `docs/hypotheses/1970-01-01-example.md` | `docs/hypotheses/1970-01-01-example.md` | `spike` |
| `scratch/README.md` | `.scratch/README.md` | `spike` |
| `llm-infra/*` | `docker/llm-infra/` | `llm-infra` |

Document templates are skeletons: `<...>` marks a value to fill, `TODO:` marks
something only a person knows, and HTML comments explain each section (delete
them once filled). The matching skill fills each file (`c4-diagrams`,
`system-design`, `quality-scenarios`, `threat-model`, `adr-write`, `spike`).

`CONTEXT.md` is a stub. Replace the heading and drop `ExampleTerm` when the first real term is chosen.

MCP definitions come from [mcp/](../mcp/), not from a template. The installer
writes `.agent-kit.lock` on the target (not a template).

## Do not copy

- This `README.md`
- Application trees (for example Spec Kit) — those come from stack skills
