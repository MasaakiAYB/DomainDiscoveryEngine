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
    capability_model = state.business_capability_model
    task_candidates = state.executable_task_candidates or []
    question = state.question_set.selected_question if state.question_set else None
    print("\n目的:")
    purposes = capability_model.purpose if capability_model else domain_model.purpose
    if not purposes:
        print("- なし")
    for purpose in purposes:
        print(f"- {purpose}")

    print("\nドメイン概念（DomainModel Concepts）:")
    if not domain_model.concepts:
        print("- なし")
    for concept in domain_model.concepts:
        print(f"- {concept.name}")

    print("\n業務タスク（DomainModel Tasks）:")
    if not domain_model.tasks:
        print("- なし")
    for task in domain_model.tasks:
        print(f"- {task.name}")

    print("\n業務ルール（BusinessRule）:")
    rules = capability_model.rules if capability_model else []
    if not rules:
        print("- なし")
    for rule in rules:
        print(f"- {rule.label}")

    print("\n判断基準（DecisionCriterion）:")
    criteria = capability_model.decision_criteria if capability_model else []
    if not criteria:
        print("- なし")
    for criterion in criteria:
        print(f"- {criterion.label}")

    print("\n業務手順（BusinessProcedure）:")
    procedures = capability_model.procedures if capability_model else []
    if not procedures:
        print("- なし")
    for procedure in procedures:
        print(f"- {procedure.label}")
        for step in procedure.steps:
            print(f"  - {step}")

    print("\n入出力仕様（InputOutputSpec）:")
    input_outputs = capability_model.input_outputs if capability_model else []
    if not input_outputs:
        print("- なし")
    for spec in input_outputs:
        inputs = ", ".join(spec.input_items) if spec.input_items else "-"
        outputs = ", ".join(spec.output_items) if spec.output_items else "-"
        print(f"- {spec.label}")
        print(f"  入力: {inputs}")
        print(f"  出力: {outputs}")

    print("\n実行可能タスク候補（ExecutableTaskCandidate）:")
    if not task_candidates:
        print("- なし")
    for candidate in task_candidates:
        print(f"- {candidate.label} ({candidate.task_type})")

    print("\n未解決事項（Unknown）:")
    unknowns = capability_model.unknowns if capability_model else domain_model.unresolved_questions
    if not unknowns:
        print("- なし")
    for unknown in unknowns:
        print(f"- {unknown}")

    print("\n次に確認したいこと:")
    if question is None:
        print("- なし")
    else:
        print(f"- {question.text}")
        if question.examples:
            print(f"  例: {', '.join(question.examples)}")
    print()


if __name__ == "__main__":
    main()
