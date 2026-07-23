#!/usr/bin/env bash
# Install all ai-toolkit skills into the Windsurf skills directory.
# Usage: ./skills.sh [target-dir]
# Default target: C:\Users\mathi\.codeium\windsurf\skills

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/skills"
DEFAULT_TARGET="/mnt/c/Users/mathi/.codeium/windsurf/skills"
TARGET_DIR="${1:-$DEFAULT_TARGET}"

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Source skills directory not found: $SOURCE_DIR"
    exit 1
fi

mkdir -p "$TARGET_DIR"

echo "Installing skills from $SOURCE_DIR to $TARGET_DIR"
echo ""

for skill in "$SOURCE_DIR"/*/; do
    name=$(basename "$skill")
    if [[ "$name" == "_template" ]]; then
        continue
    fi
    if [[ ! -f "$skill/SKILL.md" ]]; then
        echo "  ⚠️  $name: missing SKILL.md, skipping"
        continue
    fi
    echo "  ✅ $name"
    rm -rf "$TARGET_DIR/$name"
    cp -r "$skill" "$TARGET_DIR/$name"
done

echo ""
echo "Installation complete."
