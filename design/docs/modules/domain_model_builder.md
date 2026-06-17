# Module: DomainModelBuilder

## Responsibility

Build a concise, user-reviewable DomainModel from ProjectMemory.

## Input

- ProjectMemory

## Output

- DomainModel

## Rules

- Prefer confirmed items over candidate items.
- Include high-confidence candidate items when useful, but mark them as candidate.
- Do not include rejected items.
- Include unresolved questions when they affect the model.
- Use business language.

## Output sections

- purpose
- concepts
- relations
- tasks
- constraints
- assumptions
- decisions
- unresolved_questions

## Example output

```yaml
title: 実験検索支援ツール
purpose:
  - 実験条件と結果を記録し、過去の類似実験を検索・再利用できるようにする

concepts:
  - name: 実験
    description: 条件と結果を持つ業務単位
  - name: 実験条件
    description: 実験時に設定する条件
  - name: 実験結果
    description: 実験から得られる結果

relations:
  - subject: 実験
    predicate: 持つ
    object: 実験条件
  - subject: 実験
    predicate: 生み出す
    object: 実験結果

tasks:
  - name: 実験を記録する
  - name: 過去の似た実験を探す

unresolved_questions:
  - 似た実験の判定基準が未定義
```
