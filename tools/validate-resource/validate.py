#!/usr/bin/env python3
"""
validate-resource: Validates ai-toolkit resources.

Checks:
- Frontmatter YAML is valid and contains required fields
- Folder and file names are kebab-case
- No placeholder text (TODO, Agent Name, etc.)
- SKILL.md length is within limits (if applicable)

Usage:
    python validate.py                    # Validate entire repo
    python validate.py skills/flask-api   # Validate specific resource
"""

import os
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SKILL_FIELDS = {"name", "version", "author", "description", "tags", "role"}
REQUIRED_AGENT_FIELDS = {"name", "version", "author", "description", "tags", "role", "type", "language"}

PLACEHOLDERS = [
    r"Agent\s+Name",
    r"TODO\b",
    r"tu-usuario",
    r"your-name",
    r"your-user",
    r"TODO:\s*",
    r"<skill-name>",
    r"<agent-name>",
    r"INSERT_",
]

KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_frontmatter(content: str, resource_type: str) -> list[str]:
    errors = []
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter")
        return errors

    try:
        end = content.index("---", 3)
        frontmatter = yaml.safe_load(content[3:end])
    except Exception as e:
        errors.append(f"Invalid YAML frontmatter: {e}")
        return errors

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter is not a YAML mapping")
        return errors

    required = REQUIRED_AGENT_FIELDS if resource_type == "agent" else REQUIRED_SKILL_FIELDS
    missing = required - set(frontmatter.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {', '.join(sorted(missing))}")

    if frontmatter.get("author") != "Mathias Paulenko Echeverz":
        errors.append("Author must be 'Mathias Paulenko Echeverz'")

    return errors


def validate_placeholders(content: str) -> list[str]:
    errors = []
    for pattern in PLACEHOLDERS:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Placeholder detected: '{pattern}'")
    return errors


def validate_naming(path: Path) -> list[str]:
    errors = []
    rel = path.relative_to(REPO_ROOT)
    for part in rel.parts:
        if part.startswith("_") or part.startswith("."):
            continue
        name = Path(part).stem
        if not KEBAB_CASE.match(name):
            errors.append(f"Name is not kebab-case: '{name}'")
    return errors


def validate_resource(path: Path) -> list[str]:
    errors = []
    resource_type = "agent" if "agents" in path.parts else "skill"

    # Find main markdown file
    md_files = list(path.glob("*.md"))
    if not md_files:
        errors.append("No markdown file found")
        return errors

    main_file = md_files[0]
    content = main_file.read_text(encoding="utf-8")

    errors.extend(validate_frontmatter(content, resource_type))
    errors.extend(validate_placeholders(content))
    errors.extend(validate_naming(path))

    # Length check for skills
    if resource_type == "skill" and len(content.splitlines()) > 600:
        errors.append("SKILL.md exceeds 600 lines; consider externalizing content")

    return errors


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = REPO_ROOT / target

    if target_path.is_file():
        target_path = target_path.parent

    resource_dirs = []
    for subdir in ["skills", "agents", "prompts", "rules", "workflows"]:
        root = REPO_ROOT / subdir
        if not root.exists():
            continue
        for item in root.iterdir():
            if item.is_dir() and not item.name.startswith("_") and not item.name.startswith("."):
                resource_dirs.append(item)

    all_ok = True
    for d in sorted(resource_dirs):
        errors = validate_resource(d)
        if errors:
            all_ok = False
            print(f"\n❌ {d.relative_to(REPO_ROOT)}")
            for e in errors:
                print(f"   - {e}")
        else:
            print(f"✅ {d.relative_to(REPO_ROOT)}")

    if all_ok:
        print("\n✅ All resources valid.")
        sys.exit(0)
    else:
        print("\n❌ Validation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
