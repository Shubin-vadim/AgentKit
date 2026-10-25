# Get started

## Requirements

- An agent client: Cursor, Claude Code, OpenCode, or Codex.
- [uv](https://docs.astral.sh/uv/). It sets up Python 3.12+ and Pydantic on
  first use. You do not need to install uv in advance when the agent installs
  the kit: it offers to install uv and waits for your yes.
- Node.js for MCP servers launched with `npx` (Context7, codegraph, draw.io,
  Playwright) and for OpenSpec (20.19+).

## Install with your agent

You do not run commands yourself. You tell the agent what you are building,
and it does the rest.

1. Clone the repository:

    ```bash
    git clone https://github.com/Shubin-vadim/AgentKit.git
    ```

2. Open the clone in your agent: Cursor, Claude Code, OpenCode, or Codex.
3. Describe, in your own words:
    - **where** the project is (its path),
    - **what** you will build or do there,
    - **which agent** you will use in that project (optional; the agent can
      detect it).
4. The agent follows the `apply-kit` skill: it picks profiles, shows you one
   message with the client and profiles it chose and why, and installs after
   your OK.

## Examples

### A new service

<div class="chat" markdown>

<div class="chat-msg chat-user" markdown>
<span class="chat-who">You</span>

I'm starting a new FastAPI service for online orders in `~/projects/orders`.
I want ADRs and C4 diagrams from day one. I use Claude Code.
</div>

<div class="chat-msg chat-agent" markdown>
<span class="chat-who">Agent</span>

Install into `~/projects/orders`:

- **Client:** Claude Code — you said so
- **Profiles:** `core` + `architecture` (ADRs, C4, quality scenarios) +
  `engineering` (module design, Python code style)

OK, or should I change anything?
</div>

<div class="chat-msg chat-user" markdown>
<span class="chat-who">You</span>

Go ahead.
</div>

</div>

### You did not say which agent you use

The agent looks at the project for `.cursor/`, `.claude/`, `opencode.json`, or
`.codex/` and suggests what it finds. It never installs for a guessed client
without asking.

<div class="chat" markdown>

<div class="chat-msg chat-user" markdown>
<span class="chat-who">You</span>

Set up `D:\work\shop-frontend` — a React storefront, I'll be polishing the UI
and testing it in a real browser.
</div>

<div class="chat-msg chat-agent" markdown>
<span class="chat-who">Agent</span>

Install into `D:\work\shop-frontend`:

- **Client:** Cursor — found `.cursor/` in the project
- **Profiles:** `core` + `frontend` (distinctive UI) + `playwright` (drive a
  real browser)

OK, or do you use another agent there: Claude Code, OpenCode, Codex?
</div>

</div>

### Checking an idea before building it

<div class="chat" markdown>

<div class="chat-msg chat-user" markdown>
<span class="chat-who">You</span>

In `~/lab/search-test` I want to check whether Qdrant beats Postgres full-text
search on our product titles. Just an experiment. Codex.
</div>

<div class="chat-msg chat-agent" markdown>
<span class="chat-who">Agent</span>

Install into `~/lab/search-test`:

- **Client:** Codex — you said so
- **Profiles:** `core` + `spike` (hypothesis notes, throwaway code) +
  `llm-infra` (local Qdrant and Postgres in Docker)

OK?
</div>

</div>

### Adding more later

`apply-kit` is installed into every project with `core`, so you can ask the
agent there, without opening the kit again:

<div class="chat" markdown>

<div class="chat-msg chat-user" markdown>
<span class="chat-who">You</span>

We moved the repo to GitHub. Add whatever helps with pull requests and Actions.
</div>

<div class="chat-msg chat-agent" markdown>
<span class="chat-who">Agent</span>

Add `github` (the GitHub MCP server: repositories, issues, pull requests,
Actions) to this project for Claude Code? You will need
`GITHUB_PERSONAL_ACCESS_TOKEN` in your environment.
</div>

</div>

!!! tip "No Python or uv on the machine?"
    The installer runs with [uv](https://docs.astral.sh/uv/). If it is missing,
    the agent shows the exact install command and waits for your yes. If you
    decline, it can still copy the skills; rules, MCP servers, and templates
    wait until the installer can run.

## Install from the command line

Everything the agent does goes through this installer, so you can also run it
yourself:

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
