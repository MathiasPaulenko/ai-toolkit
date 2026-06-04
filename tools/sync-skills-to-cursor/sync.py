#!/usr/bin/env python3
"""
sync-skills-to-cursor: Copies selected skills to .cursor/rules/ for IDE integration.

Usage:
    python sync.py --all              # Copy all skills
    python sync.py flask-api behave-bdd  # Copy specific skills
    python sync.py --list             # List available skills
"""

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
CURSOR_DIR = REPO_ROOT / ".cursor" / "rules"


def get_skills() -> list[Path]:
    return sorted(
        d
        for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")
    )


def copy_skill(skill_dir: Path, dest_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return

    dest = dest_dir / f"{skill_dir.name}.md"
    shutil.copy(skill_md, dest)
    print(f"  ✅ {skill_dir.name}")


def main():
    parser = argparse.ArgumentParser(description="Sync skills to .cursor/rules")
    parser.add_argument("skills", nargs="*", help="Skill names to sync")
    parser.add_argument("--all", action="store_true", help="Sync all skills")
    parser.add_argument("--list", action="store_true", help="List available skills")
    args = parser.parse_args()

    available = get_skills()

    if args.list:
        print("Available skills:")
        for s in available:
            print(f"  {s.name}")
        return 0

    if not args.all and not args.skills:
        print("Usage: python sync.py --all | --list | <skill1> [skill2 ...]")
        return 1

    CURSOR_DIR.mkdir(parents=True, exist_ok=True)

    targets = available if args.all else [SKILLS_DIR / s for s in args.skills]

    for skill_dir in targets:
        if not skill_dir.exists():
            print(f"  ⚠️  Skill not found: {skill_dir.name}")
            continue
        copy_skill(skill_dir, CURSOR_DIR)

    print(f"\nSynced to: {CURSOR_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
