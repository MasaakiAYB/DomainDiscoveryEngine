# プロジェクトの方向性

DomainDiscoveryEngineは、対話から業務知識を構造化する前段エンジンです。

このプロジェクトの主な役割は、ユーザーとの対話から業務の理解を整理し、再利用可能な業務能力として扱える形にまとめることです。

## 何を整理するか

- 業務ルール（BusinessRule）
- 判断基準（DecisionCriterion）
- 業務手順（BusinessProcedure）
- 制約（Constraint）
- ドメイン概念（DomainModel の concepts）
- タスク分解
- 実務上の判断や運用ノウハウ

## このフェーズでDDEが行うこと

- 対話から業務知識を抽出する
- 業務能力モデル（BusinessCapabilityModel）を整理する
- 実行可能タスク候補（ExecutableTaskCandidate）を整理する
- 不足情報を未解決事項として明示する
- 次に確認すべき質問を日本語で提示する

## このフェーズで対象外のこと

以下の変換や生成は、このフェーズでは扱いません。

- Skill への変換
- MCP Tool への変換
- API への変換
- Workflow への変換
- Agent への変換
- UI への変換

## 位置づけ

```text
対話
↓
業務知識の構造化
↓
業務能力モデル（BusinessCapabilityModel）
↓
実行可能タスク候補（ExecutableTaskCandidate）
↓
将来の downstream 変換
```
