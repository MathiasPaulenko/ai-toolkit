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
tags: [python, flask, api]
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
tags: [python, flask, api]
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
tags: [python, flask, api]
role: developer
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("Mathias Paulenko Echeverz" in e for e in errors)


def test_validate_placeholders_detects_todo():
    content = """---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
description: TODO fill this in
tags: [python, flask, api]
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("Placeholder" in e for e in errors)


def test_validate_placeholders_clean():
    # Body mentions of TODO/<agent-name> are legit docs, not flagged.
    content = """---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Clean description
tags: [python, flask, api]
---
Body text can mention TODO or <agent-name> as documentation.
"""
    errors = v.validate_frontmatter(content, "skill")
    assert len(errors) == 0


def test_validate_frontmatter_bad_version():
    content = """---
name: Flask API
version: v1
author: Mathias Paulenko Echeverz
description: A skill
tags: [python, flask, api]
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("SemVer" in e for e in errors)


def test_validate_frontmatter_tags_not_list():
    content = """---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
description: A skill
tags: python
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("tags" in e for e in errors)


def test_validate_frontmatter_tags_too_few():
    content = """---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
description: A skill
tags: [python, flask]
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("tags" in e for e in errors)


def test_validate_frontmatter_tags_too_many():
    content = """---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
description: A skill
tags: [a, b, c, d, e, f, g, h]
---
"""
    errors = v.validate_frontmatter(content, "skill")
    assert any("tags" in e for e in errors)


def test_validate_agent_bad_type():
    content = """---
name: QA Bot
version: 1.0.0
author: Mathias Paulenko Echeverz
description: An agent
tags: [qa, testing, agent]
role: qa-bot
type: wizard
language: en
---
"""
    errors = v.validate_frontmatter(content, "agent")
    assert any("type must be one of" in e for e in errors)


def test_validate_agent_bad_language():
    content = """---
name: QA Bot
version: 1.0.0
author: Mathias Paulenko Echeverz
description: An agent
tags: [qa, testing, agent]
role: qa-bot
type: review
language: fr
---
"""
    errors = v.validate_frontmatter(content, "agent")
    assert any("language must be one of" in e for e in errors)


def test_validate_internal_links_broken(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text("See [missing](no-such-file.md) link.")
    errors = v.validate_internal_links(md)
    assert any("no-such-file.md" in e for e in errors)


def test_validate_internal_links_ok(tmp_path):
    (tmp_path / "target.md").write_text("# target")
    md = tmp_path / "doc.md"
    md.write_text("See [target](target.md) and [anchor](#section).")
    errors = v.validate_internal_links(md)
    assert len(errors) == 0


def test_validate_internal_links_skips_code_blocks(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text("Before\n```\n[fake](not-real.md)\n```\nAfter [URL]({placeholder}).")
    errors = v.validate_internal_links(md)
    assert len(errors) == 0
