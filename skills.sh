#!/usr/bin/env bash
# Install or inspect ai-toolkit skills in the Windsurf skills directory.
# Usage: ./skills.sh [--stats] [target-dir]
# Default target: C:\Users\mathi\.codeium\windsurf\skills

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/skills"
DEFAULT_TARGET="/mnt/c/Users/mathi/.codeium/windsurf/skills"

show_stats() {
    local target="${1:-$DEFAULT_TARGET}"
    if [[ ! -d "$target" ]]; then
        echo "Target directory not found: $target"
        exit 1
    fi

    local repo_skills=()
    for skill in "$SOURCE_DIR"/*/; do
        local name=$(basename "$skill")
        [[ "$name" == "_template" ]] && continue
        [[ -f "$skill/SKILL.md" ]] && repo_skills+=("$name")
    done

    local total=0 from_repo=0 extra=0 total_bytes=0
    local -a sizes=()
    local -a heaviest=()

    for skill in "$target"/*/; do
        [[ -d "$skill" ]] || continue
        local name=$(basename "$skill")
        local bytes=0
        if command -v find >/dev/null 2>&1; then
            bytes=$(find "$skill" -type f -printf '%s\n' 2>/dev/null | awk '{s+=$1} END {print s+0}')
        else
            bytes=$(du -sb "$skill" 2>/dev/null | awk '{print $1}')
        fi
        total=$((total + 1))
        total_bytes=$((total_bytes + bytes))
        sizes+=("$bytes $name")
        if [[ " ${repo_skills[*]} " == *" $name "* ]]; then
            from_repo=$((from_repo + 1))
        else
            extra=$((extra + 1))
        fi
    done

    avg=0
    if [[ $total -gt 0 ]]; then
        avg=$((total_bytes / total))
    fi

    echo "=== Skill metrics ==="
    echo "Target directory: $target"
    echo "Total skills: $total"
    echo "From ai-toolkit repo: $from_repo"
    echo "Additional skills: $extra"
    echo "Total size: $(numfmt --to=iec $total_bytes 2>/dev/null || echo "${total_bytes} bytes")"
    echo "Average size: $(numfmt --to=iec $avg 2>/dev/null || echo "${avg} bytes")"
    echo ""
    echo "Top 10 heaviest skills:"
    printf '%s\n' "${sizes[@]}" | sort -rn | head -n 10 | while read -r bytes name; do
        printf '  %-40s %10s\n' "$name" "$(numfmt --to=iec "$bytes" 2>/dev/null || echo "${bytes}B")"
    done
}

TARGET_DIR="$DEFAULT_TARGET"
STATS_MODE=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --stats|-s)
            STATS_MODE=1
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--stats|-s] [target-dir]"
            exit 0
            ;;
        *)
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

if [[ $STATS_MODE -eq 1 ]]; then
    show_stats "$TARGET_DIR"
    exit 0
fi

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
