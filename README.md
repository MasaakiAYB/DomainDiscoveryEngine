# DomainDiscoveryEngine

DomainDiscoveryEngine converts user dialogue into a structured domain model by extracting goals, concepts, tasks, relations, constraints, assumptions, decisions, and unknowns.

This project does not generate source code, deploy applications, or produce System IR. Those are future downstream components.

## MVP Scope

- Dialogue analysis
- Structured memory management
- Domain model construction
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

## Design Docs

- Detailed design overview: [design/README.md](design/README.md)
- Runtime guide: [design/runtime.md](design/runtime.md)
- Architecture notes: [design/architecture.md](design/architecture.md)
