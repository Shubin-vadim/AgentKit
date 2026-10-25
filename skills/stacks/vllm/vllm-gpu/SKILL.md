---
name: vllm-gpu
description: >-
  Deploy vLLM on a blank NVIDIA GPU Linux server (driver, Docker, NVIDIA
  Container Toolkit, official vllm/vllm-openai image). Use when the user asks
  to serve an LLM with vLLM on a GPU host that is not set up yet.
argument-hint: "Hugging Face model id, if known"
---

# vllm-gpu

Bring up an OpenAI-compatible vLLM server on an **empty NVIDIA GPU box**. Follow the catalog **PLAYBOOK.md**. Do not invent a second compose file or install a **host** CUDA toolkit.

This is not local `llm-infra` (Ollama/Qdrant on a laptop).

## Catalog

1. `docker/vllm/PLAYBOOK.md` in the current project
2. Else `$KIT_ROOT/templates/vllm/` (`AGENT_KIT_ROOT`, lock `kit_root`, or cwd if this is the kit)
3. Else say the profile is not applied (`apply-kit` with `vllm`)

## Workflow

1. **Ask once** if missing: Ubuntu 22.04 or 24.04; SSH/sudo on the box; Hugging Face model id; gated? (`HF_TOKEN` only in server `.env`); listen `127.0.0.1` vs public.

2. **API key.** Required. Prefix **`sk-local-`** plus a random suffix (playbook `openssl rand -hex 24`). Stop if `.env` has no key or the prefix is wrong. Show the key **once** to the operator. Do not print `HF_TOKEN`, `.env`, or the key again.

3. **Run the catalog PLAYBOOK.md in order.** Copy-paste those commands. Stop at the first failed check (`lspci`, `nvidia-smi`, GPU `docker run`, key prefix). Do not skip the in-container `nvidia-smi`.

4. **Prove with the playbook's small instruct model**, then change `VLLM_MODEL` and recreate for the real weights.

5. **Done** when `/v1/models` with `Authorization: Bearer` succeeds and the same call without a header is 401. Paste those HTTP outcomes, not the key.
