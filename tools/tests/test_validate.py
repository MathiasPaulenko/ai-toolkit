"""Tests for validate-resource tool."""

import sys
from pathlib import Path


# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validate-resource"))

import validate as v


def test_kebab_case_valid():
    assert v.KEBAB_CASE.match("my-skill")
    assert v.KEBAB_CASE.match("flask-api")
    assert v.KEBAB_CASE.match("a1-b2")


def test_kebab_case_invalid():
    assert not v.KEBAB_CASE.match("MySkill")
    assert not v.KEBAB_CASE.match("my_skill")
    assert not v.KEBAB_CASE.match("my--skill")
    assert not v.KEBAB_CASE.match("-my-skill")


def test_validate_frontmatter_valid():
    content = """---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
description: A great skill
tags: [python, flask]
role: developer
---
# Flask API
"""
    errors = v.validate_frontmatter(content, "skill")
    assert len(errors) == 0


def test_validate_frontmatter_missing_field():
    content = """---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
tags: [python, flask]
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("Missing" in e for e in errors)


def test_validate_frontmatter_wrong_author():
    content = """---
name: Flask API
version: 1.0.0
author: Someone Else
description: A skill
tags: [python]
role: developer
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("Mathias Paulenko Echeverz" in e for e in errors)


def test_validate_placeholders_detects_todo():
    errors = v.validate_placeholders("Some text with TODO here")
    assert len(errors) > 0


def test_validate_placeholders_clean():
    errors = v.validate_placeholders("This is clean content")
    assert len(errors) == 0
