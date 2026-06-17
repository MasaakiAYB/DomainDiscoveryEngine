from domain_discovery_engine.schemas.domain_model import (
    DomainConcept,
    DomainModel,
    DomainRelation,
    DomainTask,
)


def test_domain_model_can_be_created() -> None:
    model = DomainModel(
        project_id="demo",
        concepts=[DomainConcept(id="c1", name="実験")],
        relations=[DomainRelation(id="r1", subject="実験", predicate="持つ", object="条件")],
        tasks=[DomainTask(id="t1", name="記録する")],
    )
    assert model.concepts[0].name == "実験"


def test_domain_model_list_defaults_are_not_shared() -> None:
    first = DomainModel(project_id="a")
    second = DomainModel(project_id="b")
    first.purpose.append("test")
    assert second.purpose == []


def test_domain_model_round_trip() -> None:
    model = DomainModel(
        project_id="demo",
        concepts=[DomainConcept(id="c1", name="実験")],
        relations=[DomainRelation(id="r1", subject="実験", predicate="持つ", object="条件")],
        tasks=[DomainTask(id="t1", name="記録する")],
    )
    restored = DomainModel.model_validate(model.model_dump())
    assert restored == model
