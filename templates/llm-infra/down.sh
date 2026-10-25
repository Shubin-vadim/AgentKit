#!/usr/bin/env bash
# Stop catalog services. Usage: ./down.sh
#                               ./down.sh langfuse
#                               ./down.sh all
#                               ./down.sh all --volumes
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

VOLUME=0
TARGETS=()

for arg in "$@"; do
  if [[ "$arg" == "--volumes" || "$arg" == "-v" ]]; then
    VOLUME=1
    continue
  fi
  TARGETS+=("$arg")
done

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  TARGETS=(llm-infra)
fi

down_file() {
  local file="$1"
  local args=(-f "$file" down)
  [[ "$VOLUME" -eq 1 ]] && args+=(--volumes)
  docker compose "${args[@]}"
}

for t in "${TARGETS[@]}"; do
  case "$t" in
    llm-infra|primitives)
      echo "down llm-infra"
      down_file compose.yaml
      ;;
    langfuse)
      echo "down langfuse"
      down_file langfuse.yaml
      ;;
    mlflow)
      echo "down mlflow"
      down_file mlflow.yaml
      ;;
    all)
      echo "down all"
      down_file compose.yaml
      down_file langfuse.yaml
      down_file mlflow.yaml
      ;;
    *)
      echo "Unknown target: $t (llm-infra | langfuse | mlflow | all)" >&2
      exit 1
      ;;
  esac
done
