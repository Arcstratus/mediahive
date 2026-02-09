# MediaHive Backend

## Setup

```bash
uv sync
```

## Development Server

```bash
uv run fastapi dev
```

## Import Demo Data

```bash
uv run python bin/import_fixtures.py
```

This loads seed resources from `fixtures/resources.json` into the database.
