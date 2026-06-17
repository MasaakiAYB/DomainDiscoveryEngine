# DomainModel Schema

DomainModel is the external-facing model shown to users and passed to future downstream components.

It should be concise, reviewable, and business-language-oriented.

## DomainModel

```python
from pydantic import BaseModel

class DomainConcept(BaseModel):
    id: str
    name: str
    description: str
    status: str

class DomainRelation(BaseModel):
    id: str
    subject: str
    predicate: str
    object: str
    description: str = ""
    status: str

class DomainTask(BaseModel):
    id: str
    name: str
    description: str
    actor: str | None = None
    target_concepts: list[str] = []
    status: str

class DomainConstraint(BaseModel):
    id: str
    name: str
    description: str
    related_concepts: list[str] = []
    related_tasks: list[str] = []
    status: str

class DomainModel(BaseModel):
    title: str
    purpose: list[str]
    concepts: list[DomainConcept]
    relations: list[DomainRelation]
    tasks: list[DomainTask]
    constraints: list[DomainConstraint]
    assumptions: list[str]
    decisions: list[str]
    unresolved_questions: list[str]
```

## DomainModel output style

Use business terms, not technical terms.

Good:

```text
Experiment has experiment conditions.
Experiment produces experiment results.
```

Bad:

```text
experiments table has condition_id foreign key.
```

## Future compatibility

DomainModel should be stable enough to be used later by a Domain-to-IR Generator.

Do not include implementation-specific details such as:

- database table names
- API endpoints
- frontend component names
- cloud services
- deployment targets
