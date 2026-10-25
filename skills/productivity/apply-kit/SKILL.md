---
name: apply-kit
description: >-
  Install agent-kit skills, rules, and MCP servers into a project for any agent
  client (Cursor, Claude Code, OpenCode, Codex): pick profiles from a short
  description of the planned work and run the installer. Use when the user wants
  to install or update skills, rules, or MCP in a repo, set up the agent, or
  apply the kit.
---

# Apply kit

Install this library into **another** directory. Never install into the kit itself.

In the kit, agents reach this file through the kit's `AGENTS.md` / `CLAUDE.md`. In a target project it is installed with `core`, so profiles can be added or refreshed from there.

## Resolve paths

**Kit root** — first hit:

1. Env `AGENT_KIT_ROOT`
2. Target's `.agent-kit.lock` field `kit_root` (quoted path; older installs: `.cursor/agent-kit.lock`)
3. Current directory if it contains `scripts/kit.py` and `profiles/`
4. Otherwise ask once for the kit path

**Target** — directory the user named. If they did not: current directory, but **only if it is not the kit**. If you are in the kit, ask for the target path.

## Prepare the runner

The installer runs through [uv](https://docs.astral.sh/uv/). The user should not have to set anything up: check once, before detecting the client, and take the first step that works. Below, `$KIT` means the command this step gives you.

1. **uv is there** (`uv --version` works) → `KIT="uv run $KIT_ROOT/scripts/kit.py"`. On first use uv downloads Python 3.12+ and Pydantic into its own cache; nothing is created in the kit or the target, and no virtual environment needs activating.
2. **No uv, but Python is there** (`python --version`, `python3 --version`, or `py -3 --version` works) → ask once: "Install uv with `python -m pip install --user uv`?" On yes, run it and use step 1; if `uv` is still not on `PATH`, use `KIT="python -m uv run $KIT_ROOT/scripts/kit.py"`.
3. **Neither uv nor Python** → ask once to run the official uv installer, showing the exact command for the user's system:
   - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - macOS or Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

   On yes, run it, then use step 1. If the new shell does not see `uv` yet, use the full path the installer prints. uv fetches Python by itself.
4. **The user declines every installation** → say plainly what that costs, then offer the reduced install and do it only on yes:
   - Copy each selected skill folder (`skills/**/<name>/` in the kit, names from the chosen `profiles/*.yaml`) into the client's skills directory from the table in "Pick the client".
   - Rules, MCP servers, templates, and `.agent-kit.lock` are **not** installed: their formats differ per client and editing those config files by hand is error-prone.
   - Detect the client by looking for the folders listed in "Pick the client" instead of running `detect`.
   - Finish by listing what was skipped and saying that running the installer later (steps 1-3) completes the installation.

Never install software without an explicit yes, and never run an installer command the user has not seen.

## Pick the client

The client is the agent the user will run **in the target**, not necessarily the one you are running in. Never install for a client you guessed without saying so.

1. **The user named it** ("for Claude Code", "I use Cursor", "for the whole team: Cursor and Codex") → use that.
2. **Otherwise look at the target:** `$KIT detect --target "$TARGET"`. It lists the client folders already there (`.cursor/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.opencode/`, `opencode.json`, `.codex/`) and ends with `detected: <client>`, `detected: several (...)`, or `detected: none`.
3. **Build a suggestion:** one detected client → that client. Several → all of them (a team may use more than one). None → the client you are running in right now, if you know it.
4. **Confirm** it in the step below. A detected folder can be left over from an editor the user no longer uses, so a suggestion is never final until confirmed.

Where each client gets the files:

| Client | Skills | Rules | MCP |
|--------|--------|-------|-----|
| `cursor` | `.cursor/skills/` | `.cursor/rules/*.mdc` | `.cursor/mcp.json` |
| `claude` | `.claude/skills/` | `.claude/rules/*.md` (`paths` scoping) | `.mcp.json` |
| `opencode` | `.opencode/skills/` | `.opencode/rules/*.md` via `instructions` | `opencode.json` → `mcp` |
| `codex` | `.agents/skills/` | managed block in `AGENTS.md` | `.codex/config.toml` (trusted projects only) |

## Pick profiles

`core` is automatic. Do **not** pass `core` on the command line. Collect extra names from the user's wording (comma-separated, no spaces). Use only names that `$KIT list` prints.

| Signal in the request | Add |
|-----------------------|-----|
| spike, hypothesis, ad-hoc, experiment, "check whether X is true" | `spike` |
| architecture, C4, ADR, arc42, system design, docs for how the system works | `architecture` |
| domain model, deep modules, design the codebase (not a stack) | `engineering` |
| UI, frontend, visual design, distinctive interface, not templated aesthetics | `frontend` |
| browser automation, e2e check in a real browser, Playwright, UI debugging | `playwright` |
| GitHub, pull request, GitHub issues, GitHub Actions | `github` |
| LangGraph, StateGraph | `langgraph` |
| Spec Kit, `.specify/` | `speckit` |
| Qdrant, Langfuse, MLflow, Ollama, local Docker for LLM tools, Kafka/Redis/Postgres as AI infra | `llm-infra` |
| vLLM, GPU server inference, serve LLM on NVIDIA | `vllm` |
| SGLang, lmsysorg/sglang, GPU server inference | `sglang` |

Combine when several apply (e.g. greenfield service → `architecture,engineering`). **Spike wins** over stack profiles unless the user clearly asked to scaffold or ship the service. No matching signal → extras empty (core only).

`--force` only when the user asked to overwrite existing rules, templates, or MCP entries. `--dry-run` when they asked to preview.

## Confirm before installing

Send **one** message with everything you inferred, and wait for the answer:

> Install into `~/projects/x`:
> - **Client:** Claude Code — found `.claude/` in the project *(or: "you didn't say; I'm running in Claude Code, so I suggest it")*
> - **Profiles:** `core` + `architecture` (C4, ADR), `engineering` (module design)
>
> OK, or which client do you use there: Cursor, Claude Code, OpenCode, Codex (several are fine)?

- State where each choice came from: the user's words, a folder in the target, or your own client. Mark guesses as guesses.
- When the client is unknown (no hint from the user, nothing detected, and you don't know your own client), ask with the four options; do not install until the user picks.
- Ask profile questions in the same message, not in a second round.
- Skip this step only when the user already named the target, the client, and the profiles, and asked to go ahead.
- After the answer, run the installer with an explicit `--client`; do not rely on auto-detection.

## Run

Use the `$KIT` command from "Prepare the runner":

```bash
$KIT install --target "$TARGET" --client claude --profile architecture,engineering
```

Omit `--profile` when extras are empty. Always pass the confirmed `--client`. Quote paths. Show the exact command, then run it. If it fails, show stderr; do not copy files by hand instead (the reduced install of step 4 is only for a user who declined every installation).

## After a successful install

Tell the user to open the target in their client and to set any MCP secrets as environment variables visible to that client (`github` needs `GITHUB_PERSONAL_ACCESS_TOKEN`). Claude Code asks to approve project MCP servers on first use; Codex reads `.codex/config.toml` only after the project is trusted. Code graph: run `npx -y @colbymchenry/codegraph@1.6.2 init -y` in the target root (offer to run it). OpenSpec tree: `openspec-init` if they will write features (`init --tools none`). Commit `.agent-kit.lock` with the project.
