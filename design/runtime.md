# Runtime Guide

## Local Run

Install dependencies:

```bash
python3 -m pip install -e .[dev]
```

Run the CLI:

```bash
python -m domain_discovery_engine.interfaces.cli
```

Run in LLM mode:

```bash
DDE_ANALYZER_MODE=llm python -m domain_discovery_engine.interfaces.cli
```

## Tests

```bash
pytest
```

## Docker

Build:

```bash
docker compose build
```

Run:

```bash
docker compose run --rm dde
```

## Data Storage

By default, project data is stored under:

```text
.data/projects
```

If `DDE_DATA_DIR` is set, DDE uses that path instead. The JSON store creates parent directories when saving project memory.
Use `DDE_ANALYZER_MODE=rule_based` or `DDE_ANALYZER_MODE=llm` to switch the workflow implementation.
