# Recommended File Structure

```text
DomainDiscoveryEngine/
  README.md
  pyproject.toml
  .env.example
  .gitignore

  src/
    domain_discovery_engine/
      __init__.py
      main.py

      core/
        __init__.py
        config.py
        state.py
        workflow.py

      schemas/
        __init__.py
        memory.py
        extraction.py
        domain_model.py
        simulation.py
        question.py
        response.py

      agents/
        __init__.py
        dialogue_analyzer.py
        memory_updater.py
        domain_model_builder.py
        simulation_tester.py
        question_generator.py
        response_composer.py

      memory/
        __init__.py
        project_memory.py
        store.py
        json_store.py

      prompts/
        dialogue_analyzer.md
        memory_updater.md
        domain_model_builder.md
        simulation_tester.md
        question_generator.md
        response_composer.md

      interfaces/
        __init__.py
        cli.py
        api.py

      utils/
        __init__.py
        ids.py
        logging.py

  tests/
    test_dialogue_analyzer.py
    test_memory_updater.py
    test_domain_model_builder.py
    test_simulation_tester.py
    test_question_generator.py

  examples/
    experiment_management/
      conversation.md
      expected_memory.yaml
      expected_domain_model.yaml

    equipment_reservation/
      conversation.md
      expected_memory.yaml
      expected_domain_model.yaml
```

## Directory responsibilities

### core

Workflow orchestration and runtime state.

### schemas

Pydantic models for structured LLM input/output and internal data contracts.

### agents

LLM-powered or LLM-adjacent processing units.

### memory

ProjectMemory persistence and merge/update logic.

### prompts

Prompt templates for each agent.

### interfaces

CLI/API entry points.

### examples

Regression samples for expected behavior.
