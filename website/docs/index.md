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

## Quick start

Clone the repository, open it in your agent, and say what you are building:

> Install the kit into `~/projects/shop` — a new backend service, I use Claude Code.

Or run the installer yourself with [uv](https://docs.astral.sh/uv/):

```bash
uv run scripts/kit.py install --target ~/projects/shop --client claude --profile architecture,engineering
```
