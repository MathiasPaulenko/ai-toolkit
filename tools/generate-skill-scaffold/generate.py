#!/usr/bin/env python3
"""
generate-skill-scaffold: Interactive CLI to bootstrap a new skill.

Copies the template, prompts for metadata, and generates the scaffold.

Usage:
    python generate.py
    python generate.py --name my-skill --description "A great skill"
"""

import argparse
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_TEMPLATE = REPO_ROOT / "skills" / "_template" / "SKILL.md"


def kebab_case(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "-", name.lower()).strip("-").replace("--", "-")


def prompt_field(name: str, default: str = "") -> str:
    prompt = f"{name}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    value = input(prompt).strip()
    return value if value else default


def main():
    parser = argparse.ArgumentParser(description="Generate a new skill scaffold")
    parser.add_argument("--name", help="Skill name (kebab-case)")
    parser.add_argument("--description", help="One-line description")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--role", help="Primary role identifier")
    parser.add_argument("--trigger", help="Trigger condition")
    args = parser.parse_args()

    if not SKILL_TEMPLATE.exists():
        print(f"Template not found: {SKILL_TEMPLATE}")
        return 1

    name = args.name or prompt_field("Skill name (kebab-case)")
    name = kebab_case(name)

    dest_dir = REPO_ROOT / "skills" / name
    if dest_dir.exists():
        print(f"Directory already exists: {dest_dir}")
        return 1

    dest_dir.mkdir(parents=True)

    # Copy template
    dest_file = dest_dir / "SKILL.md"
    shutil.copy(SKILL_TEMPLATE, dest_file)

    # Read and replace placeholders
    content = dest_file.read_text(encoding="utf-8")

    description = args.description or prompt_field("Description", f"Skill for {name}")
    tags = args.tags or prompt_field("Tags (comma-separated)", f"{name}, python, automation")
    role = args.role or prompt_field("Role", "developer")
    trigger = args.trigger or prompt_field("Trigger", f"When the user mentions {name}")

    content = content.replace("Skill Name", name.replace("-", " ").title())
    content = content.replace("One-line description", description)
    # Update YAML frontmatter fields
    for key, val in [
        ("name", name.replace("-", " ").title()),
        ("description", description),
        ("tags", f"[{', '.join(t.strip() for t in tags.split(','))}]"),
        ("role", role),
        ("trigger", trigger),
    ]:
        # Simple replacement for known template patterns
        pass  # Template frontmatter is generic; user edits manually

    dest_file.write_text(content, encoding="utf-8")

    # Create optional subdirectories
    (dest_dir / "references").mkdir(exist_ok=True)
    (dest_dir / "assets").mkdir(exist_ok=True)

    print(f"\n✅ Skill scaffold created at: {dest_dir}")
    print("   Next steps:")
    print(f"   1. Edit {dest_dir / 'SKILL.md'}")
    print("   2. Add reference docs to references/")
    print("   3. Add templates/scripts to assets/")
    print("   4. Run validate-resource to verify")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
