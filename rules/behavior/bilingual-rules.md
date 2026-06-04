---
name: Bilingual Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for determining when to respond in Spanish vs English based on user context, resource type, and conversation history.
tags: [behavior, bilingual, spanish, english, i18n]
role: behavior-rules
type: rules
language: en
---

# Bilingual Rules

## 1. Default Language

- **Default to the user's language** from the current conversation.
- If the user switches language, switch with them.
- If the user uses a mix, follow their dominant language in that message.

## 2. Language Detection

| Cue | Action |
|-----|--------|
| User message is entirely in Spanish | Respond in Spanish |
| User message is entirely in English | Respond in English |
| User message mixes both | Match the language of the specific question/request |
| User explicitly requests a language | Honor the request |

## 3. Resource Content Language

- **Resource definitions** (skills, agents, prompts, rules, workflows) are written in **English** for universal reuse.
- **Comments within code examples** follow the resource's language (English for English resources).
- **User-facing explanations** of resources should match the user's language.

## 4. Code and Technical Terms

- Keep **technical terms** in English: `function`, `class`, `repository`, `endpoint`, `middleware`.
- Do not translate: `pull request`, `merge`, `commit`, `branch`, `pipeline`, `deployment`.
- Do translate: explanations, instructions, summaries, and non-technical prose.

```markdown
# Good (Spanish response)
Usa `async/await` en lugar de callbacks para manejar operaciones asíncronas.

# Bad
Usa `async/await` en lugar de `callbacks` para manejar operaciones asíncronas.
```

## 5. Consistency Within a Response

- Use **one language per response**.
- Do not switch languages mid-paragraph.
- If switching is necessary, use a clear transition.

## 6. Special Cases

| Case | Language |
|------|----------|
| Quoting user message | Keep original language |
| Citing file paths | Keep as-is (paths are language-neutral) |
| Error messages from tools | Keep original, translate if helpful |
| Generated code | Follow resource conventions (usually English comments) |

## 7. When Uncertain

- If you cannot detect the user's preferred language:
  1. Check the user's profile/settings if available.
  2. Check the workspace locale or OS language.
  3. Default to **English**.
  4. Briefly note: "Responding in English; let me know if you prefer Spanish."

## 8. Memory and Context

- Remember the user's language preference across the conversation.
- If the user corrects your language choice, update your preference.
- Store language preference in persistent memory if the system supports it.
