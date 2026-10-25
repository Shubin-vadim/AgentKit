# Local LLM infra

Copy-paste Docker commands for Qdrant, Langfuse, MLflow, Postgres, Redis, Kafka, and related AI tools. **Local machine only** — default passwords are weak on purpose.

Images follow the **current latest** line (`:latest`, `:main`, Postgres 18, Redis 8, Langfuse v4). `bash up.sh` and the compose examples pass `--pull always` so a start pulls a fresh digest.

From a project after profile `llm-infra`: `docker/llm-infra/`. From this kit without apply: `templates/llm-infra/`.

One-shot `docker run …` (no Compose): [docker-run.md](./docker-run.md).

```bash
cp .env.example .env   # once, then edit secrets
bash up.sh qdrant postgres redis
bash up.sh langfuse
bash down.sh
bash down.sh langfuse
bash down.sh all --volumes   # delete data
```

Same thing without the script (PowerShell-friendly):

```bash
docker compose -f compose.yaml --profile qdrant --profile postgres up -d --pull always
docker compose -f compose.yaml --profile ollama --profile litellm up -d --pull always
docker compose -f langfuse.yaml up -d --pull always
docker compose -f mlflow.yaml up -d --pull always
docker compose -f compose.yaml down
```

`postgres` and `pgvector` both bind **5432** — start only one. `litellm` / `open-webui` also need `--profile ollama` (or `bash up.sh`, which adds it). Langfuse and MLflow are separate Compose projects with their own Postgres/Redis; they do not reuse the primitive containers.

| Command | Port | What |
|---------|------|------|
| `bash up.sh postgres` | 5432 | PostgreSQL 18 |
| `bash up.sh pgvector` | 5432 | PostgreSQL 18 + pgvector |
| `bash up.sh redis` | 6379 | Redis 8 |
| `bash up.sh kafka` | 9092 | Kafka 4 (KRaft, no ZooKeeper). Host: `localhost:9092`. Other containers: `kafka:29092` |
| `bash up.sh qdrant` | 6333 HTTP, 6334 gRPC | Vector DB. UI: http://localhost:6333/dashboard |
| `bash up.sh minio` | 9000 S3, 9001 console | Object storage |
| `bash up.sh clickhouse` | 8123 HTTP, 9009 native | Analytics DB |
| `bash up.sh chroma` | 8100 | Chroma |
| `bash up.sh neo4j` | 7474 browser, 7687 bolt | Graph / GraphRAG. Auth `neo4j/localdevpass` |
| `bash up.sh ollama` | 11434 | Local LLM runtime. Then `docker compose -f compose.yaml --profile ollama exec ollama ollama pull llama3.2` |
| `bash up.sh phoenix` | 6006 UI, 4317 OTLP | Arize Phoenix traces |
| `bash up.sh ollama litellm` | 4000 | LiteLLM → Ollama. Header `Authorization: Bearer sk-local` |
| `bash up.sh ollama open-webui` | 3080 | Chat UI → Ollama |
| `bash up.sh langfuse` | 3100 UI, 9090 MinIO | Langfuse + its own Postgres/Redis/ClickHouse/MinIO |
| `bash up.sh mlflow` | 5000 | MLflow tracking (SQLite volume) |

Combine primitives in one line: `bash up.sh qdrant redis pgvector kafka`.

Ollama does not request a GPU here. NVIDIA: add a `deploy.resources.reservations.devices` block to the `ollama` service, or run Ollama on the host and point LiteLLM/Open WebUI at `host.docker.internal:11434`.

Langfuse UI: http://localhost:3100 — first login **`dev@example.com` / `changeme`**. Replace `ENCRYPTION_KEY` (64 hex chars: `openssl rand -hex 32`), `NEXTAUTH_SECRET`, and `SALT` in `.env` before anything leaves localhost. App images are `docker.io/langfuse/langfuse:4` (upstream’s `docker.langfuse.com` registry is often blocked). If this file drifts, use the [upstream compose](https://github.com/langfuse/langfuse/blob/main/docker-compose.yml) and keep host port **3100** for the web UI so it does not clash with other tools on 3000.
