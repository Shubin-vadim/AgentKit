---
name: llm-infra
description: >-
  Start local Docker catalogs for LLM/AI tools: Qdrant, Langfuse, MLflow,
  Postgres, Redis, Kafka, Ollama, Phoenix, MinIO, Chroma, Neo4j. Use when the
  user wants to run, copy, or look up the docker compose command for these
  services.
---

# LLM infra

The catalog is `docker/llm-infra/` after apply, or `templates/llm-infra/` inside the kit. Do not invent a compose file or a `docker run` line. Copy the matching command from `README.md` / `up.sh` / `docker-run.md`. Then run it if the user asked to start something.

## Resolve the catalog

1. `docker/llm-infra/compose.yaml` in the current project
2. Else `$KIT_ROOT/templates/llm-infra/` (`AGENT_KIT_ROOT`, lock `kit_root`, or cwd if this is the kit)
3. Else say the profile is not applied (`apply-kit` with `llm-infra`)

Need Docker Compose v2 (`docker compose`). On Windows use Git Bash for `up.sh`, or the `docker compose -f … --profile … up -d --pull always` form in PowerShell.

Working directory: the catalog folder (so `.env` and `litellm.config.yaml` resolve). `up.sh` always pulls the latest digest for the image tag.

## Commands

```bash
cp .env.example .env    # once
bash up.sh qdrant postgres redis
bash up.sh langfuse
bash up.sh mlflow
bash down.sh
bash down.sh langfuse
```

Equivalent:

```bash
docker compose -f compose.yaml --profile qdrant --profile postgres up -d --pull always
docker compose -f compose.yaml --profile ollama --profile litellm up -d --pull always
docker compose -f langfuse.yaml up -d --pull always
docker compose -f mlflow.yaml up -d --pull always
```

Map the user's words to **profile names** in `compose.yaml` (`postgres`, `pgvector`, `redis`, `kafka`, `qdrant`, `minio`, `clickhouse`, `chroma`, `neo4j`, `ollama`, `phoenix`, `litellm`, `open-webui`) or stacks `langfuse` / `mlflow`. Unknown tool: say it is not in the catalog; do not add a new service unless they asked to extend the YAML.

## Constraints

- Local only. Default passwords stay in `.env.example`. Do not commit `.env`.
- `postgres` and `pgvector` both use host **5432** — one of them, not both.
- Langfuse and MLflow are **separate Compose projects**. They do not share the primitive Postgres/Redis. Langfuse UI is **3100**, not 3000.
- `open-webui` and `litellm` need `ollama` in the same `up.sh` invocation (the script adds it). Compose one-liners must pass `--profile ollama` as well.
- Langfuse first login: `dev@example.com` / `changeme`. UI port **3100**.
- After Ollama is up, pull a model: `docker exec -it <ollama-container> ollama pull llama3.2`.
- Do not enable NVIDIA `deploy` devices unless the user has the toolkit and asked for GPU.
- Production, TLS, backups, and cloud-managed Kafka are out of scope.

Ports and URLs: `README.md` in the catalog folder. Lone `docker run …` lines: copy from `docker-run.md` in the same folder; do not reconstruct them.
