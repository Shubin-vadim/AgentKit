# SGLang (GPU server)

OpenAI-compatible server via official `lmsysorg/sglang`. **Blank Ubuntu GPU box:** follow [PLAYBOOK.md](PLAYBOOK.md) from step 0. Do not invent a second compose file.

```bash
cp .env.example .env
# set SGLANG_API_KEY=sk-local-<random>  (openssl rand -hex 24)
docker compose pull
docker compose up -d
set -a && . ./.env && set +a
curl -sS http://127.0.0.1:30000/v1/models -H "Authorization: Bearer $SGLANG_API_KEY"
```

Bind is `127.0.0.1:30000` unless you change `SGLANG_BIND`. Tunnel: `ssh -N -L 30000:127.0.0.1:30000 user@host`. Clients use the same Bearer key (`sk-local-…`).

vLLM on the same host uses port 8000 (`docker/vllm/`). Local laptop Ollama catalogs are profile `llm-infra`.
