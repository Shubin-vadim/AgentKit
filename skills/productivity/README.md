# Productivity

Shared workflow skills, not tied to code.

Source: [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity) (MIT License, Copyright (c) 2026 Matt Pocock). `grill-me` is adapted for this repository: instead of the Claude Code Skill tool it reads the neighboring `grilling` skill.

`eli5` is from [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community/tree/main/eli5) (Thariq Shihipar; plugin MIT, repo Apache-2.0). Adapted: HTML file in the OS temp directory instead of a Claude Code artifact. See [eli5/NOTICE.md](./eli5/NOTICE.md).

`caveman` is from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/main/skills/caveman) (MIT). See [caveman/NOTICE.md](./caveman/NOTICE.md).

## User-invoked

Available only when you invoke them by name (`disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[grill-me](./grill-me/SKILL.md)** — Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[handoff](./handoff/SKILL.md)** — Compact the current conversation into a handoff document so another agent can continue the work.
- **[teach](./teach/SKILL.md)** — Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or together over a meeting.
- **[wait-what](./wait-what/SKILL.md)** — Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `CONTEXT.md` vocabulary.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[eli5](./eli5/SKILL.md)** — Explain a topic like I'm 5: a HTML picture book with big visuals and few words.
- **[caveman](./caveman/SKILL.md)** — Ultra-compressed replies: drop fluff, keep technical substance, until "stop caveman".
- **[write-prompt](./write-prompt/SKILL.md)** — Compose an LLM prompt in `<Role>` / `<Task>` / `<Instructions>` tags.
- **[grilling](./grilling/SKILL.md)** — Interview the user relentlessly about a plan, decision, or idea until every branch of the design tree is resolved.
- **[writing-for-agents](./writing-for-agents/SKILL.md)** — Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
- **[apply-kit](./apply-kit/SKILL.md)** — Pick profiles from a short description and install them into a target repo for any client
