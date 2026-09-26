# 90X pipeline

Downloads raw interview data into `../.data/`, then (later) normalizes it, enriches it and generates cards.

```bash
uv sync
cp .env.example .env              # fill in values
uv run pipeline sources           # list all sources
uv run pipeline download          # everything (~19 GB)
uv run pipeline download --skip-large
uv run pipeline download --domain dsa
uv run pipeline download --domain competitive
uv run pipeline download neetcode system-design-primer
```

Re-running is safe: git sources pull, HF downloads resume, files already on disk are skipped.
`../.data/manifest.json` records what was downloaded, its size and when.

Some repos have file names Windows can't hold (`:` or `?`). Those files are written with the bad characters replaced by `_`.
