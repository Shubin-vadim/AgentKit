---
name: sglang-gpu
description: >-
  Deploy SGLang on a blank NVIDIA GPU Linux server (driver, Docker, NVIDIA
  Container Toolkit, official lmsysorg/sglang image, API key). Use when the
  user asks to serve an LLM with SGLang on a GPU host that is not set up yet.
argument-hint: "Hugging Face model id, if known"
---

# sglang-gpu

Bring up an OpenAI-compatible SGLang server on an **empty NVIDIA GPU box**. Follow the catalog **PLAYBOOK.md**. Do not invent a second compose file or install a **host** CUDA toolkit.

This is not vLLM (`vllm-gpu`) and not local `llm-infra`. Default port **30000**.

## Catalog

1. `docker/sglang/PLAYBOOK.md` in the current project
2. Else `$KIT_ROOT/templates/sglang/` (`AGENT_KIT_ROOT`, lock `kit_root`, or cwd if this is the kit)
3. Else say the profile is not applied (`apply-kit` with `sglang`)

## Workflow

1. **Ask once** if missing: Ubuntu 22.04 or 24.04; SSH/sudo on the box; Hugging Face model id; gated? (`HF_TOKEN` only in server `.env`); listen `127.0.0.1` vs public.

2. **API key.** Required. Prefix **`sk-local-`** plus a random suffix (playbook `openssl rand -hex 24`). Stop if `.env` has no key or the prefix is wrong. Show the key **once** to the operator. Do not print `HF_TOKEN`, `.env`, or the key again.

3. **Run the catalog PLAYBOOK.md in order.** Copy-paste those commands. Stop at the first failed check (`lspci`, `nvidia-smi`, GPU `docker run`, key prefix). Do not skip the in-container `nvidia-smi`. If the GPU container check already passed on this host, skip playbook §§1–4.

4. **Prove with the playbook's small instruct model**, then change `SGLANG_MODEL` and recreate for the real weights.

5. **Done** when `/v1/models` with `Authorization: Bearer` succeeds on **:30000** and the same call without a header is 401. Paste those HTTP outcomes, not the key.
