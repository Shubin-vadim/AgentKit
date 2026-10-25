# vLLM (GPU server)

OpenAI-compatible server via official `vllm/vllm-openai`. **Blank Ubuntu GPU box:** follow [PLAYBOOK.md](PLAYBOOK.md) from step 0. Do not invent a second compose file.

```bash
cp .env.example .env
# set VLLM_API_KEY=sk-local-<random>  (openssl rand -hex 24)
docker compose pull
docker compose up -d
set -a && . ./.env && set +a
curl -sS http://127.0.0.1:8000/v1/models -H "Authorization: Bearer $VLLM_API_KEY"
```

Bind is `127.0.0.1:8000` unless you change `VLLM_BIND`. Tunnel: `ssh -N -L 8000:127.0.0.1:8000 user@host`. Clients use the same Bearer key (`sk-local-…`).

Local laptop CPU/Ollama catalogs are profile `llm-infra`, not this folder.
