# Next Task: Stabilize DomainDiscoveryEngine Repository

## Context

This repository implements the first MVP of **DomainDiscoveryEngine (DDE)**.

DDE is not the full system-generation platform. It is the upstream component that turns user dialogue into a converged domain model.

Current intended pipeline:

```text
User Dialogue
  -> DialogueAnalyzer
  -> MemoryUpdater
  -> ProjectMemory
  -> DomainModelBuilder
  -> SimulationTester
  -> QuestionGenerator
  -> ResponseComposer
```

The current implementation appears to contain the core skeleton, but the repository needs stabilization before extending the domain-discovery logic.

This task focuses on repository correctness, runtime reproducibility, Docker support, and documentation alignment.

Do not redesign the domain-discovery architecture in this task.

---

## Goal

Make the repository runnable, testable, and understandable from a clean checkout.

After this task, a developer should be able to:

1. Clone the repository.
2. Read the project purpose and scope from README/design docs.
3. Run the CLI locally.
4. Run tests locally.
5. Run the project in Docker.
6. Understand that DDE outputs a `DomainModel`, not a deployed application.

---

## Scope

Implement only the following stabilization items:

1. Add or restore design documentation under `design/`.
2. Fix `pyproject.toml` README reference.
3. Add Docker runtime support.
4. Make `DDE_DATA_DIR` configuration actually work.
5. Update README with local and Docker usage.
6. Add or update tests for configuration and basic CLI/workflow execution where practical.

---

## Non Goals

Do not implement the following in this task:

- Do not add IR generation.
- Do not add application code generation.
- Do not add deployment automation beyond local Docker runtime.
- Do not add Neo4j, PostgreSQL, or external database dependencies.
- Do not replace the current rule-based agents with LLM-based agents.
- Do not introduce LangGraph yet unless it already exists in the repository.
- Do not redesign `ProjectMemory` or `DomainModel` unless needed to fix tests.

---

## Required File Changes

### 1. Add `design/README.md`

Create:

```text
design/README.md
```

It must explain:

- Project name: `DomainDiscoveryEngine`
- Abbreviation: `DDE`
- DDE's role in the larger future system
- MVP scope
- Out of scope
- Main pipeline
- Expected output

Required wording concept:

```text
DomainDiscoveryEngine is the upstream domain-discovery component of a future intent-driven system generation platform.
It does not generate or deploy applications.
Its responsibility is to converge user dialogue into a structured DomainModel.
```

Include this architecture sketch:

```text
User Dialogue
  -> DomainDiscoveryEngine
  -> DomainModel
  -> Future Domain-to-IR Generator
  -> Future Application Generator
  -> Future Deployment Engine
```

---

### 2. Add `design/architecture.md`

Create:

```text
design/architecture.md
```

It must describe these modules:

- `DialogueAnalyzer`
- `MemoryUpdater`
- `ProjectMemory`
- `DomainModelBuilder`
- `SimulationTester`
- `QuestionGenerator`
- `ResponseComposer`
- `DiscoveryWorkflow`

For each module, include:

```text
Responsibility
Input
Output
Must not do
```

Important constraints:

- `ProjectMemory` is not raw conversation history.
- `ProjectMemory` is the current understanding state.
- AI-inferred items and user-confirmed items must remain distinguishable using status/source/confidence-like fields if those fields exist.
- `SimulationTester` should detect missing information by trying to execute plausible user tasks against the current domain model.

---

### 3. Add `design/runtime.md`

Create:

```text
design/runtime.md
```

It must explain:

- How to run locally
- How to run tests
- How to run with Docker
- Where project data is stored
- How `DDE_DATA_DIR` affects storage

Include expected commands:

```bash
python -m domain_discovery_engine.interfaces.cli
pytest
```

If the actual CLI command differs, update this document and README to match the actual implementation.

---

### 4. Fix `pyproject.toml`

Current issue:

`pyproject.toml` references a README path that may not exist.

Required fix:

Use one of these approaches:

Preferred:

```toml
readme = "README.md"
```

And ensure root `README.md` exists.

Alternative:

```toml
readme = "design/README.md"
```

Only use this if `design/README.md` exists and is committed.

Preferred outcome:

- Root `README.md` exists.
- `pyproject.toml` uses `readme = "README.md"`.
- Root README links to `design/README.md` for detailed design.

---

### 5. Add or update root `README.md`

Create or update:

```text
README.md
```

It must include:

- Short project description
- MVP scope
- Out of scope
- Installation
- Local run command
- Test command
- Docker run command
- Link to `design/README.md`

Required description:

```text
DomainDiscoveryEngine converts user dialogue into a structured domain model by extracting goals, concepts, tasks, relations, constraints, assumptions, decisions, and unknowns.
```

Required scope warning:

```text
This project does not generate source code, deploy applications, or produce System IR. Those are future downstream components.
```

---

### 6. Add Docker support

Create:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

#### Dockerfile requirements

- Use a Python base image.
- Install project dependencies.
- Copy project files.
- Set a working directory.
- Default command should run the CLI or show help.
- Do not require external services.

Suggested structure:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY design ./design
COPY tests ./tests

RUN pip install --upgrade pip && pip install -e .[dev]

ENV DDE_DATA_DIR=/app/.data/projects

CMD ["python", "-m", "domain_discovery_engine.interfaces.cli"]
```

Adjust the CLI module path if the repository uses a different executable entry point.

#### docker-compose.yml requirements

- Define one service named `dde`.
- Build from current directory.
- Mount `.data` for persistence if appropriate.
- Pass `DDE_DATA_DIR`.

Example:

```yaml
services:
  dde:
    build: .
    environment:
      - DDE_DATA_DIR=/app/.data/projects
    volumes:
      - ./.data:/app/.data
    stdin_open: true
    tty: true
```

#### .dockerignore requirements

Include at least:

```text
.git
.venv
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
.data
*.pyc
```

---

### 7. Fix `DDE_DATA_DIR` configuration

Current concern:

The environment variable `DDE_DATA_DIR` appears to exist in `.env.example`, but the runtime may still use a hardcoded `.data/projects` path.

Required behavior:

- If `DDE_DATA_DIR` is set, use that path.
- If not set, default to `.data/projects`.
- Ensure the directory is created when needed.

Expected implementation concept:

```python
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    data_dir: Path = Field(default=Path(".data/projects"), alias="DDE_DATA_DIR")
```

If the project does not use `pydantic-settings`, implement equivalent environment-variable handling without adding unnecessary dependencies.

Acceptance checks:

- `DDE_DATA_DIR=/tmp/dde-data` changes the storage location.
- Without `DDE_DATA_DIR`, storage defaults to `.data/projects`.

---

### 8. Update `.env.example`

Ensure `.env.example` contains:

```text
DDE_DATA_DIR=.data/projects
```

If additional environment variables exist, keep them documented.

---

### 9. Add or update tests

Add tests only where practical and aligned with the current codebase.

Minimum expected tests:

```text
tests/test_config.py
tests/test_workflow_smoke.py
```

#### `test_config.py`

Verify:

- Default data directory is `.data/projects` or equivalent.
- `DDE_DATA_DIR` overrides the default.

#### `test_workflow_smoke.py`

Verify that one simple input can run through the workflow without raising an exception.

Suggested input:

```text
実験条件と結果を記録して、過去の似た実験を探せるようにしたい
```

Expected smoke assertions:

- A project memory object exists.
- A domain model object exists or is returned.
- At least one concept/task/unknown/question exists, depending on the actual return shape.

Do not overfit tests to exact Japanese text output.

---

## Acceptance Criteria

This task is complete only if all of the following are true:

1. `README.md` exists at repository root.
2. `design/README.md` exists.
3. `design/architecture.md` exists.
4. `design/runtime.md` exists.
5. `pyproject.toml` references an existing README file.
6. `Dockerfile` exists.
7. `docker-compose.yml` exists.
8. `.dockerignore` exists.
9. `DDE_DATA_DIR` is actually used by runtime configuration.
10. `pytest` passes locally.
11. Docker build succeeds:

```bash
docker compose build
```

12. Docker run starts the CLI or displays valid CLI help:

```bash
docker compose run --rm dde
```

13. The documentation clearly states that DDE outputs `DomainModel`, not application code or deployed systems.

---

## Suggested Commit Message

```text
Stabilize repository docs, runtime config, and Docker support
```

---

## Codex Execution Instruction

When implementing this task:

1. Read this file first.
2. Inspect the current repository before editing.
3. Make the smallest changes necessary to satisfy the acceptance criteria.
4. Do not redesign the architecture.
5. Do not implement downstream IR/code/deployment generation.
6. Run tests before finishing.
7. Report changed files and any commands that failed.

