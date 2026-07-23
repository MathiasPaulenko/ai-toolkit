---
name: jinja2-templates
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Production-grade skill for Jinja2 templating in Python. Covers syntax, inheritance, macros, filters, tests, escaping, security (autoescape, XSS), Flask/FastAPI integration, and standalone code generation.
tags: [jinja2, templates, python, flask, fastapi, html, security]
trigger: When the user asks to create, refactor, fix, or explain Jinja2 templates, filters, macros, template inheritance, escaping, XSS prevention, or integration with Flask, FastAPI, or standalone Python projects.
min_version: "3.1"
---

# Jinja2 Templates Skill

## Description

Comprehensive skill for Jinja2, the dominant templating engine in Python. Covers syntax, template inheritance, macros, custom filters and tests, escaping and XSS prevention, integration with Flask and FastAPI, and standalone usage for email generation, configuration files, and code generation.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Basic Syntax](#2-basic-syntax)
3. [Control Flow](#3-control-flow)
4. [Template Inheritance](#4-template-inheritance)
5. [Includes & Imports](#5-includes--imports)
6. [Macros](#6-macros)
7. [Filters](#7-filters)
8. [Tests](#8-tests)
9. [Escaping & Security](#9-escaping--security)
10. [Flask Integration](#10-flask-integration)
11. [FastAPI Integration](#11-fastapi-integration)
12. [Standalone Usage](#12-standalone-usage)
13. [Best Practices Checklist](#13-best-practices-checklist)
14. [Common Pitfalls](#14-common-pitfalls)
15. [References](#15-references)

## When to Invoke

- Writing or refactoring Jinja2 templates in Flask, FastAPI, or standalone Python
- Creating reusable template layouts with inheritance (`extends`, `block`)
- Building custom filters or tests for domain-specific logic
- Preventing XSS through proper escaping and `autoescape`
- Generating HTML emails, configuration files, or code via templates
- Integrating Jinja2 with Flask (`render_template`, `flash`, `url_for`)
- Integrating Jinja2 with FastAPI/Starlette (`Jinja2Templates`)
- Debugging template rendering errors or variable scope issues

---

## 1. Project Setup

### Installation

```bash
pip install Jinja2>=3.1.0

# For Flask (already bundled, but explicit for standalone)
pip install Flask

# For FastAPI
pip install fastapi starlette jinja2

# For i18n support
pip install Babel
```

### Directory Layout

```
project/
  templates/              # Jinja2 template files
    base.html
    layout_email.txt
    partials/
      header.html
      footer.html
      nav.html
    macros/
      forms.html
      alerts.html
    pages/
      home.html
      profile.html
    emails/
      welcome.txt
      welcome.html
  static/                 # CSS, JS, images (Flask/FastAPI)
  app.py                  # Application entry point
```

---

## 2. Basic Syntax

### Expressions

```jinja2
{{ variable }}
{{ variable.attribute }}
{{ variable['key'] }}
{{ function(arg1, arg2) }}
{{ user.name | upper }}
{{ items | length }}
{{ "Hello, %s" | format(name) }}
```

### Statements

```jinja2
{% if user.is_active %}
  <p>Welcome back!</p>
{% endif %}

{% for item in items %}
  <li>{{ item }}</li>
{% endfor %}
```

### Comments

```jinja2
{# This is a comment and will not appear in the output #}
```

### Whitespace Control

```jinja2
{%- if true -%}  {# Trims leading and trailing whitespace #}
  No extra whitespace
{%- endif -%}
```

Configure globally in the environment:

```python
from jinja2 import Environment

env = Environment(trim_blocks=True, lstrip_blocks=True)
```

---

## 3. Control Flow

### If / Elif / Else

```jinja2
{% if user.role == 'admin' %}
  <div class="admin-panel">...</div>
{% elif user.role == 'editor' %}
  <div class="editor-panel">...</div>
{% else %}
  <div class="user-panel">...</div>
{% endif %}
```

### Inline If (Ternary)

```jinja2
{{ 'Active' if user.is_active else 'Inactive' }}
```

### For Loop

```jinja2
{% for user in users %}
  <tr class="{{ loop.cycle('odd', 'even') }}">
    <td>{{ loop.index }}</td>
    <td>{{ user.name }}</td>
  </tr>
{% else %}
  <tr><td colspan="2">No users found</td></tr>
{% endfor %}
```

### Loop Variables

| Variable | Description |
|----------|-------------|
| `loop.index` | 1-based counter |
| `loop.index0` | 0-based counter |
| `loop.first` | True on first iteration |
| `loop.last` | True on last iteration |
| `loop.length` | Total number of items |
| `loop.cycle(...)` | Cycle through values |
| `loop.revindex` | 1-based counter from end |

### Set Variable

```jinja2
{% set total = items | sum %}
{% set alert_class = 'danger' if error else 'success' %}
```

### Block Assignments (Set with content)

```jinja2
{% set content %}
  <p>This is a multi-line block assignment.</p>
  <p>Useful for capturing HTML into a variable.</p>
{% endset %}
```

---

## 4. Template Inheritance

### Base Template

```jinja2
{# templates/base.html #}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Default Title{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
  {% block extra_css %}{% endblock %}
</head>
<body>
  {% include "partials/header.html" %}

  <main>
    {% block content %}
      <p>Default content</p>
    {% endblock %}
  </main>

  {% include "partials/footer.html" %}

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  {% block extra_js %}{% endblock %}
</body>
</html>
```

### Child Template

```jinja2
{# templates/pages/home.html #}
{% extends "base.html" %}

{% block title %}Home — My App{% endblock %}

{% block extra_css %}
  <link rel="stylesheet" href="{{ url_for('static', filename='css/home.css') }}">
{% endblock %}

{% block content %}
  <h1>Welcome, {{ user.name }}</h1>
  {% include "partials/post_list.html" %}
{% endblock %}

{% block extra_js %}
  <script src="{{ url_for('static', filename='js/home.js') }}"></script>
{% endblock %}
```

### Multiple Levels of Inheritance

```jinja2
{# templates/layouts/dashboard.html #}
{% extends "base.html" %}

{% block content %}
  <div class="dashboard-layout">
    {% block sidebar %}{% endblock %}
    <div class="dashboard-content">
      {% block dashboard_content %}{% endblock %}
    </div>
  </div>
{% endblock %}
```

### `super()` — Call Parent Block Content

```jinja2
{% block extra_js %}
  {{ super() }}
  <script src="{{ url_for('static', filename='js/analytics.js') }}"></script>
{% endblock %}
```

---

## 5. Includes & Imports

### Include

```jinja2
{% include "partials/nav.html" %}

{% include "partials/alert.html" ignore missing %}

{% include "partials/widget.html" with context %}
{% include "partials/widget.html" without context %}
```

### Import Macros

```jinja2
{% from "macros/forms.html" import render_field, render_submit %}

<form method="POST">
  {{ render_field(form.username) }}
  {{ render_field(form.email) }}
  {{ render_submit("Save") }}
</form>
```

### Import with Namespace

```jinja2
{% import "macros/forms.html" as forms %}

{{ forms.render_field(form.username) }}
{{ forms.render_field(form.email) }}
```

---

## 6. Macros

### Defining Macros

```jinja2
{# templates/macros/forms.html #}
{% macro render_field(field, label=None, extra_class="") %}
  <div class="form-group {{ extra_class }}">
    <label for="{{ field.id }}">{{ label or field.label }}</label>
    <input
      type="{{ field.type }}"
      id="{{ field.id }}"
      name="{{ field.name }}"
      value="{{ field.value | default('') }}"
      class="form-control {% if field.errors %}is-invalid{% endif %}"
    >
    {% if field.errors %}
      <div class="invalid-feedback">
        {{ field.errors | join(', ') }}
      </div>
    {% endif %}
  </div>
{% endmacro %}

{% macro render_submit(text="Submit", variant="primary") %}
  <button type="submit" class="btn btn-{{ variant }}">{{ text }}</button>
{% endmacro %}
```

### Macro with `caller` (Block Macros)

```jinja2
{% macro modal(title, id="modal") %}
  <div class="modal" id="{{ id }}">
    <div class="modal-header">
      <h5>{{ title }}</h5>
    </div>
    <div class="modal-body">
      {{ caller() }}
    </div>
  </div>
{% endmacro %}
```

```jinja2
{% call modal("Confirm Delete", id="delete-modal") %}
  <p>Are you sure you want to delete this item?</p>
  <button class="btn btn-danger">Delete</button>
{% endcall %}
```

---

## 7. Filters

### Built-in Filters

```jinja2
{{ name | upper }}
{{ name | lower }}
{{ name | capitalize }}
{{ name | title }}
{{ name | trim }}
{{ name | replace("old", "new") }}
{{ items | length }}
{{ items | join(", ") }}
{{ items | sort }}
{{ items | reverse }}
{{ items | first }}
{{ items | last }}
{{ items | unique }}
{{ number | round(2) }}
{{ price | default(0.00) }}
{{ html_content | safe }}              {# Dangerous — use with care #}
{{ user_input | escape }}              {# Force escaping #}
```

### Custom Filters (Python)

```python
# filters.py
from datetime import datetime
import markdown

def format_datetime(value, fmt="%Y-%m-%d %H:%M"):
    """Format a datetime object."""
    if value is None:
        return ""
    return value.strftime(fmt)

def markdown_filter(value):
    """Convert Markdown to HTML."""
    return markdown.markdown(value, extensions=["fenced_code"])

def currency(value, symbol="$", decimals=2):
    """Format as currency."""
    return f"{symbol}{value:,.{decimals}f}"
```

### Register in Flask

```python
from flask import Flask
from filters import format_datetime, markdown_filter, currency

app = Flask(__name__)
app.jinja_env.filters["datetime"] = format_datetime
app.jinja_env.filters["markdown"] = markdown_filter
app.jinja_env.filters["currency"] = currency
```

### Register in Standalone Jinja2

```python
from jinja2 import Environment, FileSystemLoader
from filters import format_datetime

env = Environment(loader=FileSystemLoader("templates"))
env.filters["datetime"] = format_datetime
```

### Chaining Filters

```jinja2
{{ text | trim | lower | replace(" ", "-") }}
{{ items | selectattr("active") | list | length }}
```

---

## 8. Tests

### Built-in Tests

```jinja2
{% if user is defined %}
{% if value is none %}
{% if items is iterable %}
{% if items is sequence %}
{% if items is mapping %}
{% if number is number %}
{% if text is string %}
{% if value is odd %}
{% if value is even %}
{% if value is divisibleby(3) %}
{% if value is sameas(other) %}
```

### Custom Tests

```python
# tests.py
def is_email(value):
    """Test if value looks like an email."""
    import re
    return bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", str(value)))

def is_strong_password(value):
    """Test if password meets strength criteria."""
    return (
        len(value) >= 8
        and any(c.isupper() for c in value)
        and any(c.isdigit() for c in value)
    )
```

```python
# Register in Flask
app.jinja_env.tests["email"] = is_email
app.jinja_env.tests["strong_password"] = is_strong_password
```

```jinja2
{% if form.email.data is email %}
  <span class="valid">Valid email</span>
{% endif %}
```

---

## 9. Escaping & Security

### Autoescape

Jinja2 escapes all output by default in HTML contexts. Never disable this unless you explicitly trust the source.

```jinja2
{# SAFE — autoescaped by default #}
{{ user_input }}

{# SAFE — explicit escaping #}
{{ user_input | escape }}

{# DANGEROUS — marks as safe, bypasses escaping #}
{{ user_input | safe }}

{# SAFE — if content is from a trusted Markdown parser #}
{{ markdown_content | markdown | safe }}
```

### MarkupSafe Objects

```python
from markupsafe import Markup

# Mark a string as safe programmatically
trusted_html = Markup("<strong>Hello</strong>")
```

### Disabling Autoescape (Dangerous)

```jinja2
{% autoescape false %}
  {{ raw_html }}
{% endautoescape %}
```

```python
# Flask: Disable for a specific template (avoid if possible)
from flask import render_template_string
render_template_string("...", autoescape=False)
```

### Security Checklist

- [ ] Never pass raw user input to `| safe`
- [ ] Use `Markup` only for output from trusted parsers (Markdown, Bleach)
- [ ] Keep `autoescape` enabled globally
- [ ] Sanitize HTML before marking safe (use `bleach.clean()`)
- [ ] Validate all variables before rendering

---

## 10. Flask Integration

### Rendering Templates

```python
from flask import Flask, render_template, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("pages/home.html", user=current_user, posts=posts)

@app.route("/greeting/<name>")
def greeting(name):
    return render_template_string("<h1>Hello, {{ name }}!</h1>", name=name)
```

### Template Context Processors

```python
@app.context_processor
def inject_globals():
    return {
        "app_name": "My App",
        "current_year": datetime.now().year,
    }
```

### Custom Jinja2 Environment

```python
class CustomFlask(Flask):
    def create_jinja_environment(self):
        env = super().create_jinja_environment()
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.filters["datetime"] = format_datetime
        return env
```

### URL Generation in Templates

```jinja2
<a href="{{ url_for('user.profile', user_id=user.id) }}">Profile</a>
<a href="{{ url_for('static', filename='css/main.css') }}">CSS</a>
```

---

## 11. FastAPI Integration

### Setup with Starlette

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "pages/home.html",
        {"request": request, "title": "Home", "items": [1, 2, 3]}
    )
```

### Adding Custom Filters to FastAPI

```python
templates = Jinja2Templates(directory="templates")
templates.env.filters["datetime"] = format_datetime
templates.env.tests["email"] = is_email
```

### Jinja2Context in FastAPI

```python
from starlette.middleware.base import BaseHTTPMiddleware

class TemplateContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.template_context = {
            "app_name": "My FastAPI App",
        }
        return await call_next(request)
```

---

## 12. Standalone Usage

### Email Generation

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/emails"))
template = env.get_template("welcome.txt")

body = template.render(
    user_name="John",
    activation_link="https://example.com/activate/abc123"
)
```

```jinja2
{# templates/emails/welcome.txt #}
Hello {{ user_name }},

Welcome to {{ app_name }}. Please activate your account:
{{ activation_link }}

Thanks,
The {{ app_name }} Team
```

### Configuration File Generation

```python
env = Environment(loader=FileSystemLoader("templates/configs"))
template = env.get_template("nginx.conf.j2")

config = template.render(
    server_name="api.example.com",
    port=8000,
    workers=4
)
```

### Code Generation

```python
template = env.from_string("""
class {{ class_name }}:
    def __init__(self{% for field in fields %}, {{ field.name }}: {{ field.type }}{% endfor %}):
        {% for field in fields %}
        self.{{ field.name }} = {{ field.name }}
        {% endfor %}
""")

code = template.render(
    class_name="User",
    fields=[
        {"name": "id", "type": "int"},
        {"name": "email", "type": "str"},
    ]
)
```

### In-Memory Templates

```python
from jinja2 import DictLoader

env = Environment(loader=DictLoader({
    "hello.html": "<h1>Hello, {{ name }}!</h1>",
    "goodbye.html": "<p>Goodbye, {{ name }}.</p>",
}))

template = env.get_template("hello.html")
output = template.render(name="World")
```

---

## 13. Best Practices Checklist

- [ ] Use template inheritance (`extends` + `block`) for all pages; no duplication
- [ ] Place reusable components in `partials/` and macros in `macros/`
- [ ] Keep business logic out of templates; use custom filters/tests in Python
- [ ] Enable `trim_blocks` and `lstrip_blocks` to control whitespace
- [ ] Pass only necessary data to templates; avoid leaking entire objects
- [ ] Use `| default('')` for optional variables to prevent `UndefinedError`
- [ ] Keep `autoescape` enabled; never use `| safe` on user input
- [ ] Sanitize HTML with `bleach` before marking `| safe`
- [ ] Use `{% include ... ignore missing %}` for optional partials
- [ ] Define macros in dedicated files and import with `{% from ... import %}`
- [ ] Use `loop.cycle` for alternating row classes in tables
- [ ] Use `caller()` for macros that wrap variable content
- [ ] Register filters/tests in application setup, not per-request
- [ ] Use `url_for()` (Flask) or `request.url_for()` (FastAPI) for URLs
- [ ] Pre-compile templates in production (`compiled_cache` or bytecode cache)
- [ ] Add `{% set %}` for complex logic to avoid inline repetition
- [ ] Use `super()` to extend parent blocks without replacing them entirely
- [ ] Separate email text and HTML templates (`welcome.txt` + `welcome.html`)
- [ ] Use `without context` in includes when full context is unnecessary

---

## 14. Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| `UndefinedError` | Variable not passed to template | Use `| default('')` or pass the variable |
| XSS injection | `\| safe` on untrusted input | Remove `\| safe` or sanitize with `bleach` |
| Whitespace noise | Default whitespace preservation | Enable `trim_blocks` and `lstrip_blocks` |
| Missing partial | Wrong include path or missing file | Use `ignore missing` or verify path |
| Macro not found | Missing `import` or wrong namespace | Check `{% import %}` path and namespace |
| `block` not rendering | Missing `{% extends %}` | Ensure child template extends base |
| Double escaping | Already escaped + autoescape | Trust autoescape; don't manually escape |
| Context leak | Included partial sees all variables | Use `without context` or pass explicit vars |
| Slow rendering | No template caching | Enable bytecode cache (`FileSystemBytecodeCache`) |
| Mutable default args | `default([])` with mutable | Use `default([])` is safe in Jinja2; check Python |

---

## 15. References

- [Jinja2 Documentation](https://jinja.palletsprojects.com/en/latest/)
- [Jinja2 API](https://jinja.palletsprojects.com/en/latest/api/)
- [Flask — Templating](https://flask.palletsprojects.com/en/3.0.x/templating/)
- [FastAPI — Templates](https://fastapi.tiangolo.com/advanced/templates/)
- [MarkupSafe](https://markupsafe.palletsprojects.com/en/latest/)
- [bleach (HTML sanitizer)](https://bleach.readthedocs.io/)
- Related skills: `flask-api`, `fastapi-templates`
