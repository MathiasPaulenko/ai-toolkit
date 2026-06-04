# Rules

Conjunto de reglas para estandarizar código, revisiones y comportamiento.

## Estructura

- `coding/` — Reglas de estilo, patrones y restricciones de código
- `review/` — Checklists y criterios para code review
- `behavior/` — Reglas de comportamiento del asistente (tono, formato, idioma)

## Formato

Cada rule set es un archivo `.md` con reglas numeradas o categorizadas.

Ejemplo:

```markdown
# Python Coding Rules

## General
1. Usar type hints en todas las funciones públicas
2. Máximo 80 caracteres por línea

## Imports
1. Orden: stdlib > third-party > local
2. Evitar importaciones circulares
```
