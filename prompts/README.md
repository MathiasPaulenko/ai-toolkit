# Prompts

Colección de prompts organizados por tipo.

## Estructura

- `system/` — Prompts de sistema para configurar el comportamiento base del modelo
- `task/` — Prompts para tareas específicas (refactor, testing, documentación, etc)
- `templates/` — Plantillas parametrizables para reutilizar con variables

## Convención de archivo

Cada prompt es un archivo `.md` con el siguiente formato:

```markdown
---
role: system | task | template
description: qué hace
model: gpt-4o | claude-sonnet | any
---

Contenido del prompt...
```

Usar `{{variable}}` para plantillas parametrizables.
