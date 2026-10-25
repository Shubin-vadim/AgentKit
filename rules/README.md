# Rules

Rule sources are nested here for authors, as `.mdc` files with `description`
and either `alwaysApply: true` or `globs`. `scripts/kit.py install` converts them
per client: `.cursor/rules/*.mdc`, `.claude/rules/*.md` (`globs` → `paths`),
`.opencode/rules/*.md`, or a managed block in `AGENTS.md` for Codex.

| Catalog | Profile |
|---------|---------|
| [core/](./core/) | `core` — language, skills, tests-on-request, imports-at-top, openspec, write-prompt |
| [spike/](./spike/) | `spike` — hypothesis / ad-hoc, no OpenSpec |
| [architecture/](./architecture/) | `architecture` — arc42 spine |
| [llm-infra/](./llm-infra/) | `llm-infra` — local Docker catalog for LLM tools |
| [vllm/](./vllm/) | `vllm` — vLLM on a blank NVIDIA GPU server |
| [sglang/](./sglang/) | `sglang` — SGLang on a blank NVIDIA GPU server |

A profile lists rule **basenames** (no `.mdc`) under `rules:`. Do not copy this
tree into a project by hand; use a client adapter.
