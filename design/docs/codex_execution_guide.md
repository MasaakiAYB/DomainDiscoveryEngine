# Codex Execution Guide

This document is written for Codex sessions that should implement, not redesign.

## Operating rule

Codex must treat this design package as the source of truth.

When implementing a task:

1. Read `README.md`.
2. Read `docs/file_structure.md`.
3. Read the specific task file under `docs/tasks/`.
4. Implement only the files listed in that task.
5. Do not add new architectural layers unless explicitly requested.
6. Do not implement IR generation, code generation, UI generation, or deployment.
7. Keep all public data contracts compatible with `docs/schemas/*.md`.

## Definition of done for any task

A task is done only when:

- The requested files exist.
- The code is type-hinted.
- Pydantic models validate the examples in `examples/` where applicable.
- Tests listed in the task pass.
- The implementation does not introduce out-of-scope features.

## Recommended Codex prompt pattern

Use prompts like this:

```text
Read README.md, docs/codex_execution_guide.md, docs/file_structure.md, and docs/tasks/TASK_XX_*.md.
Implement only the task described there. Do not redesign the architecture. Do not implement future phases.
Run or create the tests listed in the task. Report changed files.
```

## Implementation constraints

- Python package name: `domain_discovery_engine`
- Source root: `src/`
- Prefer Pydantic v2.
- Use JSON persistence for MVP.
- Keep LLM calls behind agent classes/functions so they can be mocked in tests.
- No database dependency in MVP.
- No web framework required in MVP.
- CLI is the first user interface.

## Out-of-scope guardrails

Do not implement:

- DomainModel to System IR conversion
- Application code generation
- Database schema generation for generated apps
- Deployment automation
- Authentication
- Multi-user collaboration
- Production observability

These are downstream systems, not DDE MVP responsibilities.
