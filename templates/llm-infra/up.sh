#!/usr/bin/env bash
# Start catalog services. Usage: ./up.sh qdrant postgres
#                               ./up.sh langfuse
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

COMPOSE=(docker compose)
if [[ -f .env ]]; then
  COMPOSE+=(--env-file .env)
fi

PROFILES=()
STACKS=()

usage() {
  echo "Usage: $0 SERVICE [SERVICE...]"
  echo "       $0 --list"
  echo
  echo "Primitives (compose.yaml profiles, project llm-infra):"
  echo "  postgres pgvector redis kafka qdrant minio clickhouse chroma neo4j ollama phoenix litellm open-webui"
  echo "Stacks (own compose file, own network):"
  echo "  langfuse mlflow"
  echo
  echo "postgres and pgvector both bind 5432 — pick one."
  echo "open-webui and litellm need ollama in the same command."
}

is_profile() {
  case "$1" in
    postgres|pgvector|redis|kafka|qdrant|minio|clickhouse|chroma|neo4j|ollama|phoenix|litellm|open-webui) return 0 ;;
    *) return 1 ;;
  esac
}

if [[ $# -eq 0 || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "${1:-}" == "--list" ]]; then
  usage
  exit 0
fi

for arg in "$@"; do
  if is_profile "$arg"; then
    PROFILES+=("$arg")
  elif [[ "$arg" == "langfuse" || "$arg" == "mlflow" ]]; then
    STACKS+=("$arg")
  else
    echo "Unknown service: $arg" >&2
    usage >&2
    exit 1
  fi
done

has_postgres=0
has_pgvector=0
for p in "${PROFILES[@]+"${PROFILES[@]}"}"; do
  [[ "$p" == "postgres" ]] && has_postgres=1
  [[ "$p" == "pgvector" ]] && has_pgvector=1
done
if [[ "$has_postgres" -eq 1 && "$has_pgvector" -eq 1 ]]; then
  echo "postgres and pgvector both use host port 5432. Start only one." >&2
  exit 1
fi

need_ollama=0
have_ollama=0
for p in "${PROFILES[@]+"${PROFILES[@]}"}"; do
  [[ "$p" == "open-webui" || "$p" == "litellm" ]] && need_ollama=1
  [[ "$p" == "ollama" ]] && have_ollama=1
done
if [[ "$need_ollama" -eq 1 && "$have_ollama" -eq 0 ]]; then
  echo "Adding profile ollama (required by open-webui / litellm)."
  PROFILES+=(ollama)
fi

if [[ ${#PROFILES[@]} -gt 0 ]]; then
  profile_args=()
  for p in "${PROFILES[@]}"; do
    profile_args+=(--profile "$p")
  done
  echo "llm-infra: ${PROFILES[*]}"
  "${COMPOSE[@]}" -f compose.yaml --project-name llm-infra "${profile_args[@]}" up -d --pull always
fi

for stack in "${STACKS[@]+"${STACKS[@]}"}"; do
  echo "$stack"
  "${COMPOSE[@]}" -f "$stack.yaml" up -d --pull always
done
