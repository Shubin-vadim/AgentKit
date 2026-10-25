# Changelog

All notable changes to Agent kit are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Fixed

- The code map in `scripts/README.md` lists the current packages.

## [0.1.0] - 2026-10-25

First release.

### Added

- **Profiles.** A profile is the install list for one kind of work: skills,
  rules, MCP servers, and templates. Included: `core` (always added unless
  `--no-core`), `architecture`, `engineering`, `frontend`, `github`,
  `langgraph`, `llm-infra`, `playwright`, `reverse-engineering`, `sglang`,
  `speckit`, `spike`, and `vllm`.
- **Skills.** Architecture documentation (ADR, C4, arc42, quality scenarios,
  threat model, review, Archify diagrams), engineering practice (domain
  modeling, module design, code review, clean code, Python code style, GoF
  patterns, API design, spec and ticket workflows), OpenSpec and Spec Kit
  workflows, frontend design, LangGraph, local LLM infrastructure, GPU serving
  with vLLM and SGLang, reverse engineering, and session helpers. Vendored
  skills keep their upstream licenses and notices.
- **Templates** copied into the target: `AGENTS.md`, `CONTEXT.md`, and an
  issue-tracker note with `core`; fill-in skeletons for arc42, C4, quality
  scenarios, threat model, and ADRs with `architecture`; hypothesis notes with
  `spike`; Docker catalogs for `llm-infra`, `vllm`, and `sglang`.
- **MCP definitions**, pinned to exact versions: Context7, codegraph, draw.io,
  Playwright, REA, and the remote GitHub server. Secrets are written as
  `${env:NAME}` and rewritten for each client.
- **`scripts/kit.py`**, one command line with `list`, `detect`, `install`,
  and `check`. Run it with `uv run` (Python 3.12+, Pydantic). The code
  follows the `python-code-style` skill and is covered by unit tests, Ruff, and
  strict mypy.
- **Four clients.** `install --client cursor|claude|opencode|codex` (or
  detected from the target, several at once allowed) writes skills, rules, and
  MCP servers where each client reads them, converts rules (path scoping for
  Claude Code, a managed `AGENTS.md` block for Codex) and MCP entries (JSON for
  Cursor, Claude Code, and OpenCode, TOML for Codex), and records the result in
  `.agent-kit.lock`. Re-running is safe: existing rules, templates, and MCP
  entries are skipped unless `--force`, and `--dry-run` writes nothing. For
  Claude Code, a missing `CLAUDE.md` is created with `@AGENTS.md`.
- **`apply-kit` skill.** Describe the work planned in a project and the agent
  picks the profiles, confirms the client and profiles with you in one message,
  and runs the installer. `AGENTS.md` points agents in this repository to it.
- Documentation: [README.md](./README.md), [CONTRIBUTING.md](./CONTRIBUTING.md),
  and [AGENTS.md](./AGENTS.md).

[Unreleased]: https://github.com/Shubin-vadim/AgentKit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Shubin-vadim/AgentKit/releases/tag/v0.1.0
