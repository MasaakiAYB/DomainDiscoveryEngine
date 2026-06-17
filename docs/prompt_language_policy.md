# Prompt Language Policy

## Default Policy

- Internal prompts are English by default.
- User-facing outputs are Japanese by default.
- Schema names and internal field names remain English.
- Domain labels from user input preserve the user's original language.
- Japanese business users are the primary target users.

## Scope Separation

### Internal prompts

Internal prompts are used for structured extraction, domain modeling, and simulation. These prompts stay in English for technical stability.

### User-facing outputs

Clarification questions and future summaries are presented in Japanese by default.

### Schemas

Schemas remain in English. Future multilingual support should be handled through configuration rather than schema translation.

## Locale Direction

The current user-facing locale default is `ja-JP`.
Future multilingual support should be added through configuration, not by changing the schema model names or field names.
