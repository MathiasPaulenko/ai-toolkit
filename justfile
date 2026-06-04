# justfile — Common commands for ai-toolkit
# Install just: https://github.com/casey/just
#
# Usage:
#   just                  # List all recipes
#   just check            # Run all quality checks
#   just validate         # Validate frontmatter and naming
#   just export           # Export skills to markdown bundle
#   just export-prompts   # Export prompts to markdown bundle

# ═══════════════════════════════════════════════════════
#  Variables
# ═══════════════════════════════════════════════════════

export_dir := "exports"
python := "python"

# ═══════════════════════════════════════════════════════
#  Discovery
# ═══════════════════════════════════════════════════════

# Default: show available recipes
default:
    @just --list --unsorted

# Show repository statistics
stats:
    @echo "=== ai-toolkit Resource Statistics ==="
    @echo ""
    @echo "Skills:      $(find skills -maxdepth 1 -type d | wc -l) dirs"
    @echo "Agents:      $(find agents -maxdepth 1 -type d | wc -l) dirs"
    @echo "Prompts:     $(find prompts -type f -name '*.md' | wc -l) files"
    @echo "Rules:       $(find rules -type f -name '*.md' | wc -l) files"
    @echo "Workflows:   $(find workflows -type f -name '*.md' | wc -l) files"
    @echo "Tools:       $(find tools -maxdepth 1 -type d | wc -l) dirs"
    @echo ""
    @echo "Total Markdown: $(find . -type f -name '*.md' | wc -l) files"
    @echo "Total Python:   $(find . -type f -name '*.py' | wc -l) files"

# List all skills with descriptions
list-skills:
    @{{python}} -c "
import os, re
for d in sorted(os.listdir('skills')):
    if d.startswith('_') or d.startswith('.'): continue
    path = f'skills/{d}/SKILL.md'
    if os.path.exists(path):
        with open(path) as f:
            content = f.read()
            desc = re.search(r'description: (.+)', content)
            print(f'  {d:25s} {desc.group(1) if desc else \"\"}')"

# ═══════════════════════════════════════════════════════
#  Validation
# ═══════════════════════════════════════════════════════

# Validate all resources in the repository
validate:
    @echo "Validating resources..."
    {{python}} tools/validate-resource/validate.py

# Check for dead external links in markdown files
check-links:
    @echo "Checking for dead links..."
    {{python}} tools/check-dead-links/check.py

# Run all quality checks (validate + links)
check: validate check-links
    @echo ""
    @echo "All checks passed"

# ═══════════════════════════════════════════════════════
#  Generation
# ═══════════════════════════════════════════════════════

# Generate a new skill scaffold (interactive)
generate-skill:
    {{python}} tools/generate-skill-scaffold/generate.py

# Generate a new agent scaffold (interactive)
generate-agent:
    @echo "Copy template: cp agents/_template/agent.md agents/<name>/agent.md"
    @echo "Follow workflow: workflows/create-new-agent.md"

# ═══════════════════════════════════════════════════════
#  Export / Bundle
# ═══════════════════════════════════════════════════════

# Export all skills to a single markdown file
export:
    @mkdir -p {{export_dir}}
    {{python}} tools/export-skills-to-md/export.py --all --output {{export_dir}}/skills-bundle.md
    @echo "Exported to {{export_dir}}/skills-bundle.md"

# Export all prompts to a single markdown file
export-prompts:
    @mkdir -p {{export_dir}}
    {{python}} tools/export-skills-to-md/export.py --output {{export_dir}}/prompts-bundle.md || true
    @echo "Use: find prompts -name '*.md' -exec cat {} + > {{export_dir}}/prompts-bundle.md"

# Export everything (skills + prompts)
export-all: export export-prompts
    @echo "All bundles created in {{export_dir}}/"

# ═══════════════════════════════════════════════════════
#  IDE Integration
# ═══════════════════════════════════════════════════════

# Sync all skills to .cursor/rules/
sync-cursor:
    {{python}} tools/sync-skills-to-cursor/sync.py --all

# Sync all skills to .claude/agents/
sync-claude:
    {{python}} tools/sync-skills-to-claude/sync.py --all

# Sync to both IDEs
sync-all: sync-cursor sync-claude
    @echo "Synced to Cursor and Claude"

# ═══════════════════════════════════════════════════════
#  Maintenance
# ═══════════════════════════════════════════════════════

# Install Python dependencies for tools
install:
    pip install -r tools/requirements.txt

# Clean generated artifacts
clean:
    rm -rf {{export_dir}}/
    rm -rf .cursor/rules/*.md
    rm -rf .claude/agents/*.md
    @echo "Cleaned exports and IDE sync artifacts"

# Update version in all resources (use with caution)
bump-version version:
    @echo "Bumping version to {{version}} — review changes before committing"
    find . -name '*.md' -exec sed -i 's/^version: .*/version: {{version}}/' {} \;

# ═══════════════════════════════════════════════════════
#  Git Helpers
# ═══════════════════════════════════════════════════════

# Quick status of repo changes
status:
    @git status --short

# Commit with conventional message
cmsg type name:
    git add .
    git commit -m "{{type}}: add {{name}}"
    @echo "Committed: {{type}}: add {{name}}"

