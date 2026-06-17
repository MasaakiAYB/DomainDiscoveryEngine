from domain_discovery_engine.agents.dialogue_analyzer import DialogueAnalyzer
from domain_discovery_engine.schemas.memory import ProjectMemory


def test_example_message_extraction() -> None:
    analyzer = DialogueAnalyzer()
    message = "実験条件と結果を記録して、過去の似た実験を探せるようにしたい"
    extraction = analyzer.analyze(message, ProjectMemory(project_id="demo"))

    assert any(item.label == "過去の似た実験を探せるようにする" for item in extraction.goals)
    assert any(item.label == "実験条件" for item in extraction.concepts)
    assert any(item.label == "実験結果" for item in extraction.concepts)
    assert any(item.label == "実験条件と結果を記録する" for item in extraction.tasks)
    assert any(item.label == "過去の似た実験を探す" for item in extraction.tasks)
    assert any(item.label == "似た実験の判定基準" for item in extraction.unknowns)
