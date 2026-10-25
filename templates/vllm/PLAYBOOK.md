# vLLM on a blank NVIDIA GPU server

One node. Ubuntu **22.04 or 24.04**. Official image `vllm/vllm-openai`. Host gets **driver + Docker + NVIDIA Container Toolkit** only — do not install a host CUDA toolkit. Every request uses `Authorization: Bearer` with a key that **must** start with `sk-local-`. Do not start the server without that key. Do not bind `0.0.0.0:8000` without a firewall — the vLLM key only covers `/v1`.

Copy this folder to the server (`docker/vllm/` after apply). Work as a user with `sudo`. Stop at the first failed check.

## 0. Once

| Ask | Default |
|-----|---------|
| Hugging Face model id | prove the stack with `Qwen/Qwen2.5-7B-Instruct`, then the real model |
| Gated model | `HF_TOKEN` in `.env` on the server — never in chat |
| Listen | `127.0.0.1:8000` + SSH tunnel. Public bind only with a firewall |
| API key | `VLLM_API_KEY` in `.env`, prefix `sk-local-`. Never in chat |
| GPUs | `nvidia-smi -L` after the driver. Tensor parallel = GPU count only if the model needs it |

```bash
. /etc/os-release
echo "$ID $VERSION_ID"
```

If `ID` is not `ubuntu`, or `VERSION_ID` is not `22.04` / `24.04`, stop.

```bash
lspci | grep -i nvidia
df -h /
```

No NVIDIA device in `lspci` → stop. Need tens of GB free for weights (70B-class is hundreds of GB).

## 1. System

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg2 ubuntu-drivers-common
```

## 2. NVIDIA driver

```bash
sudo ubuntu-drivers autoinstall
sudo reboot
```

After reboot:

```bash
nvidia-smi
```

Must show the GPU(s) and a driver version. Empty / command missing → stop; do not continue to Docker.

## 3. Docker Engine

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
```

Log out and back in (or `newgrp docker`) so `docker` works without sudo. Check: `docker info`.

## 4. NVIDIA Container Toolkit

Current install: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

```bash
sudo apt-get update && sudo apt-get install -y --no-install-recommends ca-certificates curl gnupg2

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

GPU **inside** a container (do not skip):

```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

Must list the same GPU(s). Failure → stop; vLLM will not see the device.

## 5. vLLM files

On the server, this directory (`docker/vllm/` after apply):

```bash
cp .env.example .env
KEY="sk-local-$(openssl rand -hex 24)"
sed -i "s|^VLLM_API_KEY=.*|VLLM_API_KEY=$KEY|" .env
# edit .env: VLLM_MODEL, HF_TOKEN if gated. Do not commit .env.
# Confirm prefix (must be exactly sk-local-):
grep -E '^VLLM_API_KEY=sk-local-.+' .env || { echo "VLLM_API_KEY missing or wrong prefix"; exit 1; }
mkdir -p /var/lib/vllm/hf
sudo chown "$USER:$USER" /var/lib/vllm/hf
```

Show the generated key **once** to the operator (they need it for clients), then do not print `.env` again. A key that is only `sk-local-` with nothing after the last hyphen is invalid — stop.

First run: keep the default small instruct model. After `/v1/models` is healthy, change `VLLM_MODEL` and recreate.

## 6. Start

```bash
docker compose pull
docker compose up -d
docker compose logs -f
```

Wait until logs show the OpenAI-compatible server is up. OOM / CUDA errors: smaller model, `--max-model-len`, quantization (`--quantization awq` / `fp8` if the model supports it), or `--tensor-parallel-size` equal to GPU count.

Equivalent one-shot (official flags):

```bash
set -a && . ./.env && set +a
docker run --runtime nvidia --gpus all --ipc=host --restart unless-stopped \
  -v /var/lib/vllm/hf:/root/.cache/huggingface \
  --env-file .env \
  -p 127.0.0.1:8000:8000 \
  --name vllm \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen2.5-7B-Instruct \
  --served-model-name llm \
  --api-key "$VLLM_API_KEY"
```

Need `--ipc=host` (or a large `--shm-size`) for tensor parallel.

Older host drivers: add `-e VLLM_ENABLE_CUDA_COMPATIBILITY=1` (see vLLM Docker docs).

## 7. Smoke

```bash
set -a && . ./.env && set +a
AUTH="Authorization: Bearer $VLLM_API_KEY"

curl -sS http://127.0.0.1:8000/v1/models -H "$AUTH"
curl -sS http://127.0.0.1:8000/v1/chat/completions \
  -H "$AUTH" \
  -H 'Content-Type: application/json' \
  -d '{"model":"llm","messages":[{"role":"user","content":"ping"}],"max_tokens":16}'
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/v1/models
```

A request **without** the header must fail (401). Clients: OpenAI SDK `api_key=sk-local-…`, `base_url=http://127.0.0.1:8000/v1`.

From a laptop (localhost bind):

```bash
ssh -N -L 8000:127.0.0.1:8000 user@server
```

Then the same curls against `http://127.0.0.1:8000`.

## 8. Done

- `docker compose ps` is up
- `/v1/models` with `Authorization: Bearer sk-local-…` returns the served name
- The same call without a header is 401
- A short chat completion returns tokens
- Port is `127.0.0.1` unless they set a firewall in front of a public bind

Out of scope: Kubernetes, AMD ROCm, TLS/nginx, multi-node.

Docs: https://docs.vllm.ai/en/stable/deployment/docker.html
