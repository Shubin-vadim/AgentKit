---
title: Home
hide:
  - navigation
  - toc
---

# Agent kit

**Portable agent skills, rules, MCP servers, and templates — installed by your agent, for your client.**

Tell your agent what you are building. It picks the matching profiles from this
library and installs them into your project for **Cursor**, **Claude Code**,
**OpenCode**, or **Codex**.

[Get started](getting-started.md){ .md-button .md-button--primary }
[Browse skills](skills.md){ .md-button }
[View on GitHub](https://github.com/Shubin-vadim/AgentKit){ .md-button }

## Just tell your agent

No commands to learn. Open this repository in your agent and describe the
project you are about to build and where it lives:

<div class="chat" markdown>

<div class="chat-msg chat-user" markdown>
<span class="chat-who">You</span>

I'm starting a new FastAPI service for online orders in `~/projects/orders`.
I want ADRs and C4 diagrams from day one. I use Claude Code.
</div>

<div class="chat-msg chat-agent" markdown>
<span class="chat-who">Agent</span>

Install into `~/projects/orders`:

- **Client:** Claude Code — you said so
- **Profiles:** `core` + `architecture` (ADRs, C4, quality scenarios) +
  `engineering` (module design, Python code style)

OK, or should I change anything?
</div>

<div class="chat-msg chat-user" markdown>
<span class="chat-who">You</span>

Go ahead.
</div>

<div class="chat-msg chat-agent" markdown>
<span class="chat-who">Agent</span>

Done. Skills, rules, and MCP servers are in `~/projects/orders` in Claude
Code's layout, recorded in `.agent-kit.lock`. Open the project in Claude Code
and approve the MCP servers when it asks.
</div>

</div>

The agent picks the profiles, asks you to confirm, and runs the installer.
[See more examples](getting-started.md#examples).

<div class="grid cards" markdown>

-   :material-robot-outline:{ .lg .middle } **Agent-driven install**

    ---

    Describe the project; the `apply-kit` skill picks profiles, confirms the
    client and profiles with you, and runs the installer.

    [:octicons-arrow-right-24: Get started](getting-started.md)

-   :material-swap-horizontal:{ .lg .middle } **One source, four clients**

    ---

    Skills, rules, and MCP entries are written once and converted to each
    client's layout, then recorded in `.agent-kit.lock`.

    [:octicons-arrow-right-24: How it works](how-it-works.md)

-   :material-sitemap-outline:{ .lg .middle } **Architecture out of the box**

    ---

    arc42, C4, ADRs, quality scenarios, and threat models, with skills that
    write them and fill-in templates to start from.

    [:octicons-arrow-right-24: Profiles](profiles.md)

-   :material-pin-outline:{ .lg .middle } **Pinned MCP servers**

    ---

    Context7, codegraph, draw.io, Playwright, REA, and GitHub, pinned to exact
    versions. Secrets stay in environment variables.

    [:octicons-arrow-right-24: Get started](getting-started.md#after-installing)

</div>

??? note "Prefer the terminal?"

    The agent runs the same installer you can call yourself with
    [uv](https://docs.astral.sh/uv/):

    ```bash
    uv run scripts/kit.py install --target ~/projects/orders --client claude --profile architecture,engineering
    ```
