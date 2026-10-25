# Contributing

This repository is a portable agent-asset library. Do not apply it into itself.
`scripts/kit.py install` installs profiles for Cursor, Claude Code, OpenCode, or
Codex; open the target in that client afterwards. Keep source assets
client-neutral so every adapter can translate them.

Names must be unique across the whole library, not only inside one catalog:

- skill folder (the directory that contains `SKILL.md`)
- rule basename (`foo` in `foo.mdc`)
- MCP fragment basename (`foo` in `foo.json`)

A profile YAML is the only install list. Keys: `skills`, `rules`, `mcp`, `templates`. Omit a key if that profile adds none.

Template entries are paths under `templates/`. `src => dest` when the path in the project differs; otherwise dest is src.

```yaml
templates:
  - AGENTS.md
  - architecture/docs/C4.md => docs/C4.md
```

`uv run scripts/kit.py check` verifies uniqueness and that every profile entry exists.

`scripts/kit.py install` writes `.agent-kit.lock` in the target root (kit path,
revision, clients, installed items). Commit it with the target project.

Write rules as `.mdc` with `description`, and either `alwaysApply: true` or
`globs`; the installer converts them for each client. Write MCP secrets as
`${env:NAME}`; the installer rewrites them per client. When a rule or skill
refers to an installed skill, name the skill (`follow skill write-prompt`)
instead of a client path such as `.cursor/skills/...`.

Nothing from the library is installed into this repository itself. An agent
working here finds `apply-kit` through the "Installing into a project" section
of [AGENTS.md](./AGENTS.md) and [CLAUDE.md](./CLAUDE.md).
