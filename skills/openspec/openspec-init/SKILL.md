---
name: openspec-init
description: >-
  Create the project's openspec/ tree with the OpenSpec CLI. Use when openspec/
  is missing, or the user asks to initialize OpenSpec.
---

# OpenSpec init

Scaffold `openspec/` only. Kit skills (`openspec-*`) are already in the project's skills folder.

## Workflow

1. If `openspec/config.yaml` or `openspec/specs/` exists, stop: already initialized.
2. Need Node.js **20.19+**. If missing, say so and stop.
3. Prefer `openspec` on PATH. Else `npx -y @fission-ai/openspec@latest`.
4. From the **project root** (not this kit):

   ```bash
   openspec init --tools none --profile core
   ```

   `--tools none` must stay. It creates `openspec/` and does **not** rewrite the client's skills or commands folders.
5. Confirm `openspec/specs/` and `openspec/changes/` exist. Show `openspec --version` if the CLI reports it.

Do not invent an `openspec/` tree by hand. The CLI writes `.openspec.yaml` metadata later changes need.
