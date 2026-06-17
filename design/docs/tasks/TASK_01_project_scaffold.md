# TASK 01: Project scaffold

## Goal

Create the Python package scaffold for DomainDiscoveryEngine.

## Files to create

```text
pyproject.toml
.env.example
.gitignore
src/domain_discovery_engine/__init__.py
src/domain_discovery_engine/main.py
src/domain_discovery_engine/core/__init__.py
src/domain_discovery_engine/core/config.py
src/domain_discovery_engine/core/state.py
src/domain_discovery_engine/core/workflow.py
src/domain_discovery_engine/schemas/__init__.py
src/domain_discovery_engine/agents/__init__.py
src/domain_discovery_engine/memory/__init__.py
src/domain_discovery_engine/prompts/.gitkeep
src/domain_discovery_engine/interfaces/__init__.py
src/domain_discovery_engine/utils/__init__.py
src/domain_discovery_engine/utils/ids.py
src/domain_discovery_engine/utils/logging.py
tests/__init__.py
```

## Requirements

- Package name must be `domain_discovery_engine`.
- Use `src/` layout.
- `pyproject.toml` must include dependencies for:
  - pydantic
  - pyyaml
  - pytest
  - python-dotenv
- Do not add LangGraph yet.
- Do not add web framework dependencies yet.

## Acceptance criteria

- `python -m domain_discovery_engine.main` runs without error.
- `pytest` runs, even if there are no real tests yet.
