# Get started

## Requirements

- An agent client: Cursor, Claude Code, OpenCode, or Codex.
- [uv](https://docs.astral.sh/uv/). It sets up Python 3.12+ and Pydantic on
  first use. You do not need to install uv in advance when the agent installs
  the kit: it offers to install uv and waits for your yes.
- Node.js for MCP servers launched with `npx` (Context7, codegraph, draw.io,
  Playwright) and for OpenSpec (20.19+).

## Install with your agent

1. Clone the repository:

    ```bash
    git clone https://github.com/Shubin-vadim/AgentKit.git
    ```

2. Open the clone in your agent and describe the target project: its path, the
   work planned there, and which client you use in it.

    > Install the kit into `~/projects/shop`. It is a new FastAPI service, and
    > I want ADRs and C4 diagrams. I use Cursor.

3. The agent follows the `apply-kit` skill. It picks profiles from your
   description, detects the client from the target if you did not name it,
   and confirms everything in one message before installing.

If you decline installing uv, the agent can still copy the skills. Rules, MCP
servers, and templates then wait until the installer can run.

## Install from the command line

```bash
uv run scripts/kit.py list
uv run scripts/kit.py install --target /path/to/repo --client claude --profile architecture,engineering
uv run scripts/kit.py install --target /path/to/repo --client cursor,codex --profile spike --dry-run
```

`core` is always added unless you pass `--no-core`. Without `--client`, the
installer detects the client from the target. `--dry-run` writes nothing, and
`--force` overwrites existing rules, templates, and MCP entries.

## Where the files go

| `--client` | Skills | Rules | MCP |
|------------|--------|-------|-----|
| `cursor` | `.cursor/skills/` | `.cursor/rules/*.mdc` | `.cursor/mcp.json` |
| `claude` | `.claude/skills/` | `.claude/rules/*.md` | `.mcp.json` |
| `opencode` | `.opencode/skills/` | `.opencode/rules/*.md` via `instructions` | `opencode.json` |
| `codex` | `.agents/skills/` | managed block in `AGENTS.md` | `.codex/config.toml` |

The installer also writes `.agent-kit.lock` in the target root. Commit it with
the project.

## After installing

1. Open the target project in the client you installed for.
2. Set MCP secrets as environment variables that client can see, for example
   `GITHUB_PERSONAL_ACCESS_TOKEN` for the `github` profile.
3. Approve project MCP servers when Claude Code asks; trust the project in
   Codex so it reads `.codex/config.toml`.
4. Index the code graph once:

    ```bash
    npx -y @colbymchenry/codegraph@1.6.2 init -y
    ```

5. If `openspec/` is missing and you will write features, ask the agent to run
   `openspec-init`.

!!! tip "Typical sets"
    `architecture` for design documents; `engineering` for code structure;
    `spike` for hypotheses and experiments; add `frontend`, `playwright`, or
    `github` as needed. See [Profiles](profiles.md).
