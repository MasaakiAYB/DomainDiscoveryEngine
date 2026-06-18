from __future__ import annotations

from pathlib import Path

from domain_discovery_engine.core.config import AppConfig
from domain_discovery_engine.core.workflow import DiscoveryWorkflow
from domain_discovery_engine.memory.json_store import JsonProjectMemoryStore
from domain_discovery_engine.schemas.memory import ProjectMemory


def main() -> None:
    config = AppConfig()
    store = JsonProjectMemoryStore(base_dir=Path(config.data_dir))
    workflow = DiscoveryWorkflow()

    try:
        project_id = input("Project ID: ").strip() or "default"
    except EOFError:
        print()
        return
    memory = store.load(project_id) or ProjectMemory(project_id=project_id)

    while True:
        try:
            user_message = input("You> ").strip()
        except EOFError:
            print()
            break
        if user_message == "/exit":
            break
        if not user_message:
            continue

        state = workflow.run_turn(memory, user_message)
        memory = state.project_memory
        store.save(memory)
        _print_state(state)


def _print_state(state) -> None:
    domain_model = state.domain_model
    task_candidates = state.executable_task_candidates or []
    question = state.question_set.selected_question if state.question_set else None
    print("\nCurrent purpose:")
    for purpose in domain_model.purpose:
        print(f"- {purpose}")
    print("\nConcepts:")
    for concept in domain_model.concepts:
        print(f"- {concept.name}")
    print("\nTasks:")
    for task in domain_model.tasks:
        print(f"- {task.name}")
    print("\nUnresolved questions:")
    for unknown in domain_model.unresolved_questions:
        print(f"- {unknown}")
    print("\nExecutable task candidates:")
    for candidate in task_candidates:
        print(f"- {candidate.label} ({candidate.task_type})")
    print("\nNext question:")
    if question is None:
        print("- None")
    else:
        print(f"- {question.text}")
        if question.examples:
            print(f"  例: {', '.join(question.examples)}")
    print()


if __name__ == "__main__":
    main()
