# docker run (one service)

Copy-paste. Local only. Same ports as `compose.yaml`. Stop: `docker rm -f NAME`.

`--pull always` fetches the current latest tag. Do not run `postgres` and `pgvector` together (both use 5432). Langfuse is several containers — use `bash up.sh langfuse`, not a single `docker run`. Langfuse UI: http://localhost:3100 (`dev@example.com` / `changeme`).

## Qdrant — http://localhost:6333/dashboard

```bash
docker run -d --name llm-qdrant --pull always --restart unless-stopped -p 6333:6333 -p 6334:6334 -v llm-qdrant:/qdrant/storage docker.io/qdrant/qdrant:latest
```

## Postgres 18

```bash
docker run -d --name llm-postgres --pull always --restart unless-stopped -p 5432:5432 -e POSTGRES_USER=llm -e POSTGRES_PASSWORD=llm -e POSTGRES_DB=llm -v llm-postgres:/var/lib/postgresql docker.io/postgres:18-alpine
```

## Postgres + pgvector

```bash
docker run -d --name llm-pgvector --pull always --restart unless-stopped -p 5432:5432 -e POSTGRES_USER=llm -e POSTGRES_PASSWORD=llm -e POSTGRES_DB=llm -v llm-pgvector:/var/lib/postgresql docker.io/pgvector/pgvector:pg18
```

## Redis 8

```bash
docker run -d --name llm-redis --pull always --restart unless-stopped -p 6379:6379 -v llm-redis:/data docker.io/redis:8-alpine redis-server --appendonly yes
```

## Kafka (KRaft) — localhost:9092

```bash
docker run -d --name llm-kafka --hostname kafka --pull always --restart unless-stopped -p 9092:9092 -e KAFKA_NODE_ID=1 -e KAFKA_PROCESS_ROLES=broker,controller -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:29092,PLAINTEXT_HOST://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092 -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka:9093 -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 -e CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk -e KAFKA_LOG_DIRS=/var/lib/kafka/data -v llm-kafka:/var/lib/kafka/data docker.io/apache/kafka:latest
```

## MinIO — S3 :9000, console :9001

```bash
docker run -d --name llm-minio --pull always --restart unless-stopped -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=miniosecret -v llm-minio:/data docker.io/minio/minio:latest server /data --console-address ":9001"
```

## ClickHouse — HTTP :8123

```bash
docker run -d --name llm-clickhouse --pull always --restart unless-stopped -p 8123:8123 -p 9009:9000 -e CLICKHOUSE_USER=clickhouse -e CLICKHOUSE_PASSWORD=clickhouse -e CLICKHOUSE_DB=default -v llm-clickhouse:/var/lib/clickhouse docker.io/clickhouse/clickhouse-server:latest
```

## Chroma — :8100

```bash
docker run -d --name llm-chroma --pull always --restart unless-stopped -p 8100:8000 -e IS_PERSISTENT=TRUE -v llm-chroma:/chroma/chroma docker.io/chromadb/chroma:latest
```

## Neo4j — browser :7474  (neo4j / localdevpass)

```bash
docker run -d --name llm-neo4j --pull always --restart unless-stopped -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/localdevpass -e NEO4J_PLUGINS='["apoc"]' -v llm-neo4j:/data docker.io/neo4j:latest
```

## Ollama — :11434

```bash
docker run -d --name llm-ollama --pull always --restart unless-stopped -p 11434:11434 -v llm-ollama:/root/.ollama docker.io/ollama/ollama:latest
docker exec -it llm-ollama ollama pull llama3.2
```

## Phoenix — :6006

```bash
docker run -d --name llm-phoenix --pull always --restart unless-stopped -p 6006:6006 -p 4317:4317 -v llm-phoenix:/phoenix/data docker.io/arizephoenix/phoenix:latest
```

## MLflow — http://localhost:5000

```bash
docker run -d --name llm-mlflow --pull always --restart unless-stopped -p 5000:5000 -v llm-mlflow:/mlflow ghcr.io/mlflow/mlflow:latest mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:////mlflow/mlflow.db --default-artifact-root /mlflow/artifacts
```

## Open WebUI — :3080 (Ollama already on the host)

```bash
docker run -d --name llm-open-webui --pull always --restart unless-stopped -p 3080:8080 --add-host=host.docker.internal:host-gateway -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -v llm-open-webui:/app/backend/data ghcr.io/open-webui/open-webui:main
```

## LiteLLM — :4000

From this folder so `litellm.config.yaml` mounts. That file talks to `http://ollama:11434` (Compose network). For a lone `docker run`, point it at the host Ollama:

```bash
docker run -d --name llm-litellm --pull always --restart unless-stopped -p 4000:4000 --add-host=host.docker.internal:host-gateway -e LITELLM_MASTER_KEY=sk-local -v "${PWD}/litellm.config.yaml:/app/config.yaml:ro" ghcr.io/berriai/litellm:main-stable --config /app/config.yaml --port 4000 --num_workers 1
```

Then either put Ollama on a Docker network named `ollama`, or change `api_base` in the config to `http://host.docker.internal:11434`. Header: `Authorization: Bearer sk-local`.

## Langfuse

Several containers (web, worker, Postgres, Redis, ClickHouse, MinIO). Use Compose:

```bash
bash up.sh langfuse
```
