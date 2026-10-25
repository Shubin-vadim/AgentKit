# Contributing

Contributions of skills, rules, MCP definitions, templates, and profiles are
welcome. The full guide is
[CONTRIBUTING.md](https://github.com/Shubin-vadim/AgentKit/blob/main/CONTRIBUTING.md);
the essentials:

1. Keep asset names unique across the library: skill folder, rule basename, and
   MCP fragment basename.
2. Add every new asset to an explicit profile. Optional capabilities belong in
   optional profiles, not in `core`.
3. MCP fragments hold a launch definition or a remote URL only. Reference
   secrets as `${env:NAME}` and pin package versions.
4. When vendoring a skill, keep its upstream license and notice files, and add
   it to the "Skill sources" table in the README. The [skill catalog](skills.md)
   reads its source column from that table.
5. Write documentation in English.

## Checks

```bash
uv run scripts/kit.py check
uv run scripts/kit.py install --target /tmp/scratch --client claude --profile architecture --dry-run
uv run --group dev ruff check scripts tests
uv run --group dev python -m mypy scripts tests
uv run --group dev python -m pytest
```

## Licenses

Agent kit is released under the
[MIT License](https://github.com/Shubin-vadim/AgentKit/blob/main/LICENSE).
Vendored skills keep their upstream licenses; the [skill catalog](skills.md)
links each one to its source.
