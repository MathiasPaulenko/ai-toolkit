#!/usr/bin/env python3
"""
export-skills-to-md: Concatenates selected skills into a single markdown file.

Useful for manual context pasting into LLM chat interfaces.

Usage:
    python export.py --all --output skills-bundle.md
    python export.py flask-api behave-bdd --output my-skills.md
    python export.py --list
"""

import argparse
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"


def get_skills() -> list[Path]:
    return sorted(
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")
    )


def read_skill(skill_dir: Path) -> str | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None
    return skill_md.read_text(encoding="utf-8")


def build_bundle(skills: list[Path], title: str = "Skills Bundle") -> str:
    lines = [f"# {title}", "", f"_Generated on {datetime.now().isoformat()}_", ""]

    for skill_dir in skills:
        content = read_skill(skill_dir)
        if content is None:
            continue

        lines.append(f"## Skill: {skill_dir.name}")
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Export skills to a single markdown file")
    parser.add_argument("skills", nargs="*", help="Skill names to export")
    parser.add_argument("--all", action="store_true", help="Export all skills")
    parser.add_argument("--output", "-o", default="skills-bundle.md", help="Output file")
    parser.add_argument("--title", default="Skills Bundle", help="Bundle title")
    parser.add_argument("--list", action="store_true", help="List available skills")
    args = parser.parse_args()

    available = get_skills()

    if args.list:
        print("Available skills:")
        for s in available:
            print(f"  {s.name}")
        return 0

    if not args.all and not args.skills:
        print("Usage: python export.py --all -o bundle.md | --list | <skill1> [skill2 ...]")
        return 1

    targets = available if args.all else [SKILLS_DIR / s for s in args.skills]
    bundle = build_bundle(targets, title=args.title)

    output_path = Path(args.output)
    output_path.write_text(bundle, encoding="utf-8")
    print(f"✅ Exported {len(targets)} skills to: {output_path.absolute()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
