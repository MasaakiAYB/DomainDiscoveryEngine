# Codex Prompt Examples

## TASK 01 prompt

```text
Read README.md, docs/codex_execution_guide.md, docs/file_structure.md, and docs/tasks/TASK_01_project_scaffold.md.
Implement only TASK 01. Do not implement schemas or agents yet. Do not add LangGraph or web framework dependencies. Run pytest and report changed files.
```

## TASK 02 prompt

```text
Read README.md, docs/codex_execution_guide.md, docs/tasks/TASK_02_schemas_memory.md, and docs/schemas/project_memory.md.
Implement only TASK 02. Use Pydantic v2. Create tests listed in the task. Do not implement persistence or agents.
```

## TASK 06 prompt

```text
Read README.md, docs/codex_execution_guide.md, docs/tasks/TASK_06_extraction_schema_and_analyzer_stub.md, and docs/modules/dialogue_analyzer.md.
Implement only TASK 06. Use a rule-based MVP stub if no LLM client exists. The example Japanese message must pass tests. Do not implement memory update or workflow.
```

## TASK 10 prompt

```text
Read README.md, docs/codex_execution_guide.md, docs/workflow.md, docs/tasks/TASK_10_workflow_and_cli.md, and all schema docs.
Implement only TASK 10 by wiring existing components. Do not change public schemas unless tests prove a mismatch with the design docs. The CLI must persist ProjectMemory and print the current model plus next question each turn.
```
