# DomainDiscoveryEngine

DomainDiscoveryEngine structures business knowledge from dialogue and converts it into business capability models and executable task candidates.

This project does not generate source code, deploy applications, or produce System IR. Downstream forms such as Skills, MCP Tools, APIs, Workflows, Agents, and UIs are future components.

## 日本語概要

DomainDiscoveryEngineは、対話から業務知識を構造化するエンジンです。

このプロジェクトでは、プロジェクトメモリ（ProjectMemory）に蓄積した対話内容から、ドメインモデル（DomainModel）と業務能力モデル（BusinessCapabilityModel）を整理します。

特に、以下の業務知識を明示的に扱います。

- 業務ルール（BusinessRule）
- 判断基準（DecisionCriterion）
- 業務手順（BusinessProcedure）
- 入出力仕様（InputOutputSpec）
- 実行可能タスク候補（ExecutableTaskCandidate）
- 未解決事項（Unknown）
- 制約（Constraint）

これらを人がレビューしやすい形にまとめ、後続の設計や自動化検討で再利用しやすくすることが目的です。

Skill / MCP Tool / API / Workflow / Agent への変換は将来の downstream であり、このフェーズの対象外です。

## プロジェクトの位置づけ

DomainDiscoveryEngine は、実装生成の前に業務理解を安定化させる前段エンジンです。

対話から得た情報をそのままコード化するのではなく、まず業務の構造、判断、手順、入出力、未解決事項を分離して整理します。

そのため、このリポジトリの主な成果物は、レビュー可能な業務知識モデルです。

## 何を抽出するか

CLI 実行では、主に次の情報を抽出・表示します。

- 目的
- ドメイン概念
- 業務タスク
- 業務ルール（BusinessRule）
- 判断基準（DecisionCriterion）
- 業務手順（BusinessProcedure）
- 入出力仕様（InputOutputSpec）
- 実行可能タスク候補（ExecutableTaskCandidate）
- 未解決事項（Unknown）

業務能力モデル（BusinessCapabilityModel）は、これらの情報を再利用しやすい単位で束ねるための表現です。

## Business Capability Direction

ドメインモデル（DomainModel）は概念とタスクの把握に向いていますが、それだけでは実務上の判断条件やレビュー基準が不足します。

そのため DDE では、業務ルール（BusinessRule）、判断基準（DecisionCriterion）、業務手順（BusinessProcedure）、入出力仕様（InputOutputSpec）、実行可能タスク候補（ExecutableTaskCandidate）まで含めた業務能力モデル（BusinessCapabilityModel）を重視します。

## MVP Scope

- Dialogue analysis
- Structured memory management
- Domain model construction
- Business capability model construction
- Executable task candidate extraction
- Simulation-based missing-information detection
- Follow-up question generation
- CLI-based workflow
- JSON persistence for `ProjectMemory`

## Out Of Scope

- System IR generation
- Application code generation
- Deployment automation beyond local Docker runtime
- External databases and production infrastructure

## Installation

```bash
python3 -m pip install -e .[dev]
```

## Local Run

```bash
python -m domain_discovery_engine.interfaces.cli
```

対話を入力すると、CLI は業務知識を解析し、ドメインモデル（DomainModel）、業務能力モデル（BusinessCapabilityModel）、未解決事項（Unknown）、次の確認質問を表示します。

LLM mode:

```bash
DDE_ANALYZER_MODE=llm python -m domain_discovery_engine.interfaces.cli
```

## Test

```bash
pytest
```

## Docker

```bash
docker compose build
docker compose run --rm dde
```

Docker 設定がある場合も、基本的な使い方はローカル実行と同様です。

## Data Storage

Project data is stored under `.data/projects` by default. Set `DDE_DATA_DIR` to change the storage root.
Set `DDE_ANALYZER_MODE=rule_based` or `DDE_ANALYZER_MODE=llm` to switch between implementations.

## Prompt And Language Policy

- The target user language is Japanese.
- Internal prompts use English for technical stability in domain modeling and simulation tasks.
- User-facing questions and summaries are Japanese by default.
- User-provided business terms are preserved in their original language.
- `DDE_USER_LOCALE=ja-JP` controls the user-facing language.

## Design Docs

- Detailed design overview: [design/README.md](design/README.md)
- Runtime guide: [design/runtime.md](design/runtime.md)
- Architecture notes: [design/architecture.md](design/architecture.md)
- Project direction: [docs/project_direction.md](docs/project_direction.md)
- Business capability model: [docs/business_capability_model.md](docs/business_capability_model.md)
