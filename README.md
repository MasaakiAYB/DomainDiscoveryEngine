# DomainDiscoveryEngine

DomainDiscoveryEngine structures business knowledge from dialogue and converts it into business capability models and executable task candidates.

This project does not generate source code, deploy applications, or produce System IR. Downstream forms such as Skills, MCP Tools, APIs, Workflows, Agents, and UIs are future components.

## MVP Scope

- Dialogue analysis
- Structured memory management
- Domain model construction
- Business capability model construction
- Executable task candidate extraction
- Simulation-based missing-information detection
- Follow-up question generation
- CLI-based workflow
- JSON persistence for `ProjectMemory`

## Out Of Scope

- System IR generation
- Application code generation
- Deployment automation beyond local Docker runtime
- External databases and production infrastructure

## Installation

```bash
python3 -m pip install -e .[dev]
```

## Local Run

```bash
python -m domain_discovery_engine.interfaces.cli
```

LLM mode:

```bash
DDE_ANALYZER_MODE=llm python -m domain_discovery_engine.interfaces.cli
```

## Test

```bash
pytest
```

## Docker

```bash
docker compose build
docker compose run --rm dde
```

## Data Storage

Project data is stored under `.data/projects` by default. Set `DDE_DATA_DIR` to change the storage root.
Set `DDE_ANALYZER_MODE=rule_based` or `DDE_ANALYZER_MODE=llm` to switch between implementations.

## Prompt And Language Policy

- The target user language is Japanese.
- Internal prompts use English for technical stability in domain modeling and simulation tasks.
- User-facing questions and summaries are Japanese by default.
- User-provided business terms are preserved in their original language.
- `DDE_USER_LOCALE=ja-JP` controls the user-facing language.

## Design Docs

- Detailed design overview: [design/README.md](design/README.md)
- Runtime guide: [design/runtime.md](design/runtime.md)
- Architecture notes: [design/architecture.md](design/architecture.md)
