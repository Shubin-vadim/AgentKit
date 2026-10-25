# Agents

Skills live in the client's skills folder (`.cursor/skills/`, `.claude/skills/`, `.opencode/skills/`, or `.agents/skills/`) as `{name}/SKILL.md`. Invoke by folder name. If the folder is missing, the skill is not installed — do not invent it.

## Language

**Glossary** — before naming a domain concept, read `CONTEXT.md`. Use those terms exactly. A new synonym: add the term to `CONTEXT.md` first, then use it.

## Session

**Handoff** — ending the session, switching agents, or compacting work: `handoff`.

**Grill** — a plan, design, or decision still has an open branch: `grill-me`. Domain docs in play: `grill-with-docs` if installed.

**Wait-what** — the last message did not land: `wait-what`.

**ELI5** — a dead-simple picture explainer of how something works: `eli5`.

**Caveman** — terse session style, less tokens: `caveman`. Off: "stop caveman" or "normal mode".

## Work

**Apply kit** — install or refresh this library on a project from a short description: `apply-kit`.

**OpenSpec** — TZ or a change from a description: `openspec-propose` (Cursor: `/opsx-propose`). Fuzzy idea first: `openspec-explore`. No `openspec/` folder yet: `openspec-init`. Implement: `openspec-apply-change`. Archive: `openspec-archive-change`. Spike / hypothesis / ad-hoc: `spike` if installed — do not propose until the user says it is a feature.

**Review** — a diff, branch, or PR against standards and spec: `code-review`. Spec source: active `openspec/changes/` then `docs/agents/issue-tracker.md` if it exists.

**Research** — a question that needs primary sources and a citable note: `research`. Library/API docs: Context7 (`resolve-library-id`, then `query-docs`) when that MCP is connected.

**Spike** — plan how to check a claim (data optional); run in `.scratch/` only if asked: `spike` if installed.

**LLM infra** — local Docker for Qdrant, Langfuse, MLflow, Postgres, Redis, Kafka, Ollama: `llm-infra` if installed (`docker/llm-infra/`, `bash up.sh qdrant`).

**vLLM GPU** — serve a model on a blank NVIDIA GPU server: `vllm-gpu` if installed. Playbook: `docker/vllm/PLAYBOOK.md`. Client key prefix `sk-local-`.

**SGLang GPU** — same, SGLang on port 30000: `sglang-gpu` if installed. Playbook: `docker/sglang/PLAYBOOK.md`. Same key prefix.

**Code graph** — to understand an area of code (where something lives, who calls it, what a change affects), call `codegraph_explore` when the codegraph MCP is connected; it returns the relevant source and call paths in one step. Prefer it over grep and reading files one by one. If it reports no index, run `npx -y @colbymchenry/codegraph@1.6.2 init -y` in the project root once, then retry.

**Prompt** — write, draft, or compose a prompt for a model: `write-prompt`.

**ADR** — a hard-to-reverse choice with a real trade-off: `adr-write` if installed.

**C4** — system, container, or context diagrams: `c4-diagrams` if installed.

**System design** — arc42 document (`docs/arc42.md`): `system-design` if installed.

**Deepen modules** — scan for shallow modules, HTML report, then grill: `improve-codebase-architecture` if installed.

**Frontend** — new UI or reshaping an existing one, distinctive not templated: `frontend-design` if installed.

## Writing for agents

Editing skills, this file, or `CLAUDE.md`: `writing-for-agents`.
