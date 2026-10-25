# Agent instructions

## Repository purpose

This repository is a **library** of portable agent assets. It is not an
application template and must never be applied to itself. Use it to select a
small, explicit profile for a separate target repository.

The profile YAML files are the sole install lists. Skills, rules, templates,
and MCP definitions are client-neutral source assets. `scripts/kit.py install`
writes them in the layout of the chosen client (Cursor, Claude Code, OpenCode,
or Codex) and records the result in the target's `.agent-kit.lock`.

## Installing into a project

When the user asks to install, apply, or set up skills, rules, or MCP in another
project (often by describing the work planned there), read and follow
[skills/productivity/apply-kit/SKILL.md](./skills/productivity/apply-kit/SKILL.md).
It picks profiles from the description and runs the installer. Installing changes
only the target project, so the Validation steps below do not apply: do not run
`check`, Ruff, mypy, or pytest after an install.

## Working rules

1. Read [CONTRIBUTING.md](./CONTRIBUTING.md) before adding or changing a skill, rule,
   MCP fragment, template, or profile.
2. Keep asset names globally unique: a skill folder name, rule basename, and MCP
   fragment basename must each be unique across the library.
3. Add every new asset to an explicit profile. Do not broaden `core` without a
   clear reason: optional capabilities belong in optional profiles.
4. MCP fragments contain a stdio launch definition or a remote `url` endpoint
   only. Reference secrets as `${env:NAME}`; never commit credentials, API
   keys, local absolute paths, or vendor checkouts.
5. Preserve upstream license and attribution files when vendoring an external
   skill. Pin executable MCP packages when a matching skill depends on their
   tool contract.
6. Do not alter unrelated uncommitted work. Keep documentation links relative
   to the document that contains them.

## Validation

This section is only for changes to the kit itself (skills, rules, MCP
fragments, templates, profiles, scripts), not for installing into a project.

Run the library check after any asset or profile change:

```bash
uv run scripts/kit.py check
```

Then preview an installation into a separate, disposable target, once per
client you touched:

```bash
uv run scripts/kit.py install --target /path/to/target --client claude --profile reverse-engineering --no-core --dry-run
```

The scripts run with uv (`uv run` installs Python 3.12+ and Pydantic on first
use). Python code follows the `python-code-style` skill; before finishing a
change, run Ruff, mypy, and pytest as in [scripts/README.md](./scripts/README.md).
Never pass this repository as `--target`.

## REA profile

`reverse-engineering` is optional. It supplies the version-pinned REA MCP
definition and `reverse-engineer-anything` skill for authorized analysis of
shipped artifacts or runtime behavior. A client adapter installs them. It does
not install Ghidra, IDA, JADX, or any other native-analysis engine.
