# Profiles

A profile lists portable skill folder names, rule basenames, MCP fragment names,
and templates. `scripts/kit.py install` writes those assets in the layout of the
chosen client (Cursor, Claude Code, OpenCode, Codex) and copies templates into
the project.

Template line: path under `templates/`, or `src => dest` when the project path differs.

Skills, rules, MCP, or templates not listed stay in the library (`teach`, `to-questionnaire`). Profile `vllm` is vLLM on a blank NVIDIA GPU server; profile `sglang` is SGLang on a blank NVIDIA GPU server; profile `spike` is hypothesis/ad-hoc; profile `llm-infra` is the local Docker catalog for Qdrant/Langfuse/MLflow and related tools; profile `frontend` is distinctive UI (`frontend-design`); profile `github` is the remote GitHub MCP server; profile `playwright` is Playwright MCP for browser automation. Example: `--profile architecture,engineering` or `--profile spike` or `--profile llm-infra` or `--profile frontend` or `--profile vllm` or `--profile sglang`.

`reverse-engineering` supplies the REA MCP definition and matching skill for
authorized inspection of shipped artifacts and runtime behavior. Example:
`--profile reverse-engineering`.

The YAML is the subset. An adapter performs installation. See
[CONTRIBUTING.md](../CONTRIBUTING.md).
