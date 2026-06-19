# 業務能力モデル（BusinessCapabilityModel）

## 目的

業務能力モデル（BusinessCapabilityModel）は、対話から抽出した業務知識を、再利用しやすい構造に整理するためのモデルです。

## 構成要素

- 目的
- ドメイン概念
- 業務タスク
- 業務ルール（BusinessRule）
- 判断基準（DecisionCriterion）
- 業務手順（BusinessProcedure）
- 入出力仕様（InputOutputSpec）
- 制約（Constraint）
- 実行可能タスク候補（ExecutableTaskCandidate）
- 未解決事項（Unknown）

## 業務ルール（BusinessRule）

業務の実行時に守る条件、除外規則、優先ルール、例外条件などを表します。

例:

- 対象外候補は除外する
- 条件を満たさない場合はレビュー対象にする

## 判断基準（DecisionCriterion）

人や将来の自動処理が判断に使う観点を表します。

例:

- 仕様一致
- 単位整合
- 過去実績との差分

## 業務手順（BusinessProcedure）

業務の進め方やステップ列を表します。

例:

1. 候補を収集する
2. 条件を比較する
3. レビュー要否を判断する

## 入出力仕様（InputOutputSpec）

業務やタスクに必要な入力と、期待する出力を表します。

例:

- 入力: 品名、仕様、単位、数量、候補カタログ
- 出力: 評価結果、レビュー対象一覧

## 実行可能タスク候補（ExecutableTaskCandidate）

将来、Skill / MCP Tool / API / Workflow / Agent / UI などへ変換可能な候補タスクを表します。

このフェーズでは候補を整理するだけであり、実際の生成は行いません。

## ドメインモデル（DomainModel）との関係

ドメインモデル（DomainModel）は、業務の概念・関係・タスクを簡潔に示すためのモデルです。

業務能力モデル（BusinessCapabilityModel）は、それを拡張し、業務ルール、判断基準、業務手順、入出力仕様、実行可能タスク候補まで含めて整理します。

## 対象外

このモデル自体は、以下を直接生成するものではありません。

- 実装済み Skill
- 実装済み MCP Tool
- 実装済み API
- 実装済み Workflow
- 実装済み Agent
- 実装済み UI
