#!/usr/bin/env python3
"""
validate-resource: Validates ai-toolkit resources.

Checks:
- Frontmatter YAML is valid and contains required fields
- version is SemVer, tags is a list of kebab-case strings
- Agent type/language are valid enum values
- Folder and file names are kebab-case
- No placeholder text in frontmatter values
- Relative links in .md files resolve to existing files
- SKILL.md length is within limits (if applicable)

Usage:
    python validate.py                    # Validate entire repo
    python validate.py skills/flask-api   # Validate specific resource
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FIELDS = {"name", "version", "author", "description", "tags"}
REQUIRED_AGENT_FIELDS = REQUIRED_FIELDS | {"role", "type", "language"}

AGENT_TYPES = {"governance", "coding", "review", "creative", "research", "automation"}
AGENT_LANGUAGES = {"en", "es"}

AUTHOR = "Mathias Paulenko Echeverz"

# Matched against frontmatter values only — resource bodies legitimately
# mention these tokens (e.g. scaffold workflows that use <agent-name>).
PLACEHOLDERS = [
    r"Agent\s+Name",
    r"Skill\s+Name",
    r"TODO\b",
    r"tu-usuario",
    r"your-name",
    r"your-user",
    r"INSERT_",
]

KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
MD_LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")

SKIP_PREFIXES = ("_", ".")

# categories whose resources are directories with a main file (agent.md / SKILL.md)
DIR_CATEGORIES = ("skills", "agents")
# categories where every .md file is a resource
FILE_CATEGORIES = ("prompts", "rules", "workflows")


def validate_frontmatter(content: str, resource_type: str) -> list[str]:
    errors = []
    if not content.startswith("---"):
        return ["Missing YAML frontmatter"]

    try:
        end = content.index("---", 3)
        frontmatter = yaml.safe_load(content[3:end])
    except (ValueError, yaml.YAMLError) as e:
        return [f"Invalid YAML frontmatter: {e}"]

    if not isinstance(frontmatter, dict):
        return ["Frontmatter is not a YAML mapping"]

    required = REQUIRED_AGENT_FIELDS if resource_type == "agent" else REQUIRED_FIELDS
    missing = required - set(frontmatter.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {', '.join(sorted(missing))}")

    if frontmatter.get("author") != AUTHOR:
        errors.append(f"Author must be '{AUTHOR}'")

    version = frontmatter.get("version")
    if version is not None and not SEMVER.match(str(version)):
        errors.append(f"version must be SemVer (X.Y.Z), got '{version}'")

    tags = frontmatter.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or not 3 <= len(tags) <= 7:
            errors.append("tags must be a list of 3-7 items")
        elif not all(isinstance(t, str) and KEBAB_CASE.match(t) for t in tags):
            errors.append("tags must be kebab-case strings")

    if resource_type == "agent":
        agent_type = frontmatter.get("type")
        if agent_type is not None and agent_type not in AGENT_TYPES:
            errors.append(f"type must be one of: {', '.join(sorted(AGENT_TYPES))}")
        language = frontmatter.get("language")
        if language is not None and language not in AGENT_LANGUAGES:
            errors.append(
                f"language must be one of: {', '.join(sorted(AGENT_LANGUAGES))}"
            )

    for key, value in frontmatter.items():
        if not isinstance(value, str):
            continue
        for pattern in PLACEHOLDERS:
            if re.search(pattern, value, re.IGNORECASE):
                errors.append(f"Placeholder in '{key}': '{pattern}'")

    return errors


def validate_naming(path: Path) -> list[str]:
    errors = []
    rel = path.relative_to(REPO_ROOT)
    for part in rel.parts:
        stem = Path(part).stem
        if stem.startswith(SKIP_PREFIXES):
            continue
        if not KEBAB_CASE.match(stem):
            errors.append(f"Name is not kebab-case: '{stem}'")
    return errors


def validate_internal_links(path: Path) -> list[str]:
    """Check that relative markdown links point to existing files.

    Skips links inside fenced code blocks and template-style targets
    ({var}, ${var}, <var>), which are documentation placeholders.
    """
    errors = []
    text = path.read_text(encoding="utf-8")
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for url in MD_LINK.findall(line):
            if url.startswith(("http://", "https://", "mailto:")):
                continue
            if "{" in url or "$" in url or "<" in url:
                continue
            if not (path.parent / url).resolve().exists():
                errors.append(f"Broken internal link: {url}")
    return errors


def find_main_file(folder: Path, category: str) -> Path | None:
    preferred = "agent.md" if category == "agents" else "SKILL.md"
    candidate = folder / preferred
    if candidate.exists():
        return candidate
    md_files = sorted(folder.glob("*.md"))
    return md_files[0] if md_files else None


def collect_resources() -> list[tuple[str, Path]]:
    """Return (kind, path) for every resource: ('dir', folder) or ('file', md)."""
    resources = []

    for category in DIR_CATEGORIES:
        root = REPO_ROOT / category
        if not root.exists():
            continue
        for item in sorted(root.iterdir()):
            if item.is_dir() and not item.name.startswith(SKIP_PREFIXES):
                resources.append(("dir", item))

    for category in FILE_CATEGORIES:
        root = REPO_ROOT / category
        if not root.exists():
            continue
        for f in sorted(root.rglob("*.md")):
            if f.name.lower() == "readme.md":
                continue
            rel_parts = f.relative_to(root).parts
            if any(p.startswith(SKIP_PREFIXES) for p in rel_parts):
                continue
            resources.append(("file", f))

    return resources


def validate_resource(kind: str, path: Path) -> list[str]:
    errors = []
    resource_type = "agent" if "agents" in path.parts else "skill"

    if kind == "dir":
        main_file = find_main_file(path, path.parent.name)
        if main_file is None:
            return ["No markdown file found"]
    else:
        main_file = path

    content = main_file.read_text(encoding="utf-8")

    errors.extend(validate_frontmatter(content, resource_type))
    errors.extend(validate_naming(path))

    if resource_type == "skill" and len(content.splitlines()) > 1000:
        errors.append("SKILL.md exceeds 1000 lines; consider externalizing content")

    return errors


LINK_CHECK_SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "exports"}


def collect_markdown_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix == ".md" else []
    return sorted(
        f
        for f in root.rglob("*.md")
        if not any(p in LINK_CHECK_SKIP_DIRS for p in f.parts)
    )


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = (REPO_ROOT / target).resolve()

    resources = collect_resources()
    if target != ".":
        resources = [
            (k, p)
            for k, p in resources
            if p.resolve() == target_path or target_path in p.resolve().parents
        ]
        if not resources:
            print(f"No resources found under '{target}'")
            sys.exit(1)

    all_ok = True
    for kind, path in resources:
        errors = validate_resource(kind, path)
        if errors:
            all_ok = False
            print(f"\n❌ {path.relative_to(REPO_ROOT)}")
            for e in errors:
                print(f"   - {e}")
        else:
            print(f"✅ {path.relative_to(REPO_ROOT)}")

    scan_root = target_path if target != "." else REPO_ROOT
    link_failures = False
    for md_file in collect_markdown_files(scan_root):
        errors = validate_internal_links(md_file)
        if errors:
            link_failures = True
            print(f"\n❌ {md_file.relative_to(REPO_ROOT)} (internal links)")
            for e in errors:
                print(f"   - {e}")
    if link_failures:
        all_ok = False

    if all_ok:
        print("\n✅ All resources valid.")
        sys.exit(0)
    else:
        print("\n❌ Validation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
