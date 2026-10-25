# Scripts

One command line, [kit.py](./kit.py), backed by the [agent_kit](./agent_kit/)
package. Run it with [uv](https://docs.astral.sh/uv/): `uv run` reads the
dependencies declared at the top of `kit.py` (Python 3.12+, Pydantic) and sets
them up on first use, from any directory. Without uv, install Pydantic 2 into a
Python 3.12+ environment and run `python scripts/kit.py`.

| Command | Purpose |
|---------|---------|
| `list` | Profiles available in this kit |
| `detect --target DIR` | Which agent clients a project already uses (reports only) |
| `install --target DIR ...` | Install profiles into a project for one or more clients |
| `check` | Validate the library: unique names, every profile entry exists |

```bash
uv run scripts/kit.py list
uv run scripts/kit.py detect --target /path/to/repo
uv run scripts/kit.py install --target /path/to/repo --client cursor --profile architecture
uv run scripts/kit.py install --target /path/to/repo --client claude --profile architecture,engineering --dry-run
uv run scripts/kit.py install --target /path/to/repo --client opencode --profile engineering --force
uv run scripts/kit.py install --target /path/to/repo --client codex,cursor --profile llm-infra
uv run scripts/kit.py check
```

Never pass this repository as `--target`.

## install

Copies the skills, rules, MCP servers, and templates listed in the chosen
profiles into a target project, in the layout of each client:

| `--client` | Skills | Rules | MCP |
|------------|--------|-------|-----|
| `cursor` | `.cursor/skills/{name}/` | `.cursor/rules/{name}.mdc` | `.cursor/mcp.json` |
| `claude` | `.claude/skills/{name}/` | `.claude/rules/{name}.md`, `globs` → `paths` | `.mcp.json` (`type: http` for remote) |
| `opencode` | `.opencode/skills/{name}/` | `.opencode/rules/{name}.md`, listed in `opencode.json` `instructions` | `opencode.json` → `mcp` |
| `codex` | `.agents/skills/{name}/` | one managed block in `AGENTS.md` | managed block in `.codex/config.toml` |

MCP fragments write secrets as `${env:NAME}`; the installer rewrites that for
each client (`${NAME}` for Claude Code, `{env:NAME}` for OpenCode,
`bearer_token_env_var` / `env_vars` for Codex).

`core` is always included unless `--no-core`. Without `--client` the client is
detected from the target (`.cursor/`, `.claude/`, `opencode.json`, `.codex/`);
when none or several match, pass it explicitly. `detect` only reports what it
finds, so an agent can confirm the client with the user before installing.
Several clients at once: `--client cursor,claude`.

Skill folders are updated file by file and stale files are removed. Rules, templates, and MCP entries that already
exist are skipped unless `--force`. Codex servers defined outside the managed
block are never touched. For `claude`, a missing `CLAUDE.md` is created with
`@AGENTS.md` so Claude Code versions that do not read `AGENTS.md` directly
still load it. `.agent-kit.lock` in the target root records the kit revision,
clients, and installed items; commit it with the project.

## Development

The scripts follow the `python-code-style` skill: Pydantic models, Sphinx
docstrings, one class per file, Ruff, strict mypy, and a unit test for every
public method.

```bash
uv sync --group dev
uv run --group dev ruff format scripts tests
uv run --group dev ruff check scripts tests
uv run --group dev python -m mypy scripts tests
uv run --group dev python -m pytest
```

## Code map

| Package | Responsibility |
|---------|----------------|
| [cli/](./agent_kit/cli/) | `KitCli`: commands, options, and wiring of everything below |
| [models/](./agent_kit/models/) | Pydantic models: layout, profiles, rules, MCP servers, install plan, lock |
| [library/](./agent_kit/library/) | Library roots, asset lookup by name, profile, rule, and MCP parsing, `check` |
| [clients/](./agent_kit/clients/) | One adapter per client and the registry; adding a client is one subclass |
| [files/](./agent_kit/files/) | Writes with dry run and `--force`, managed blocks, skill folder sync |
| [services/](./agent_kit/services/) | Install planning and running, `.agent-kit.lock` |
| [errors.py](./agent_kit/errors.py), [utils.py](./agent_kit/utils.py) | Error hierarchy and small helpers |
