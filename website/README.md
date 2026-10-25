# Website

Source of <https://shubin-vadim.github.io/AgentKit/>, built with
[Zensical](https://zensical.org/).

| Path | Role |
|------|------|
| [zensical.toml](./zensical.toml) | Site configuration and navigation |
| [docs/](./docs/) | Hand-written pages |
| [build_catalog.py](./build_catalog.py) | Generates `docs/skills.md` and `docs/profiles.md` |
| [site_catalog/](./site_catalog/) | The generator: reads skills, profiles, and the README "Skill sources" table |
| [tests/](./tests/) | Tests for the generator |

`docs/skills.md` and `docs/profiles.md` are generated and not committed. Edit
the skills, profiles, or README instead.

## Preview

From the repository root:

```bash
uv run website/build_catalog.py
uv run --no-project --with zensical==0.0.72 zensical serve -f website/zensical.toml
```

Open <http://localhost:8000/AgentKit/>. On Windows with Application Control, run
`python -m zensical` instead of `zensical`.

## Checks

```bash
uv run --group dev ruff check website
uv run --group dev python -m pytest website/tests -p no:cacheprovider
MYPYPATH="scripts:website" uv run --group dev python -m mypy website/site_catalog website/build_catalog.py website/tests
```

## Publishing

[.github/workflows/pages.yml](../.github/workflows/pages.yml) runs the checks,
generates the catalog, builds the site, and deploys it to GitHub Pages on every
push to `main`. In the repository settings, Pages must use
**Source: GitHub Actions**.
