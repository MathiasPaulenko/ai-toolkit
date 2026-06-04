# Makefile — Common commands for ai-toolkit
# Alternative to justfile for systems without `just` installed.
#
# Usage:
#   make                  # Show available targets
#   make check            # Run all quality checks
#   make validate         # Validate frontmatter and naming
#   make export           # Export skills to markdown bundle

export_dir := exports
python := python

# Default: show available targets
.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  make stats          Show repository statistics"
	@echo "  make validate       Validate all resources"
	@echo "  make check-links    Check for dead external links"
	@echo "  make check          Run all quality checks"
	@echo "  make export         Export skills to markdown bundle"
	@echo "  make export-prompts Export prompts to markdown bundle"
	@echo "  make export-all     Export everything"
	@echo "  make sync-cursor    Sync skills to .cursor/rules/"
	@echo "  make sync-claude    Sync skills to .claude/agents/"
	@echo "  make install        Install Python dependencies"
	@echo "  make test           Run tool tests"
	@echo "  make clean          Clean generated artifacts"

stats:
	@echo "=== ai-toolkit Resource Statistics ==="
	@echo ""
	@echo "Skills:      $$(find skills -maxdepth 1 -type d | wc -l) dirs"
	@echo "Agents:      $$(find agents -maxdepth 1 -type d | wc -l) dirs"
	@echo "Prompts:     $$(find prompts -type f -name '*.md' | wc -l) files"
	@echo "Rules:       $$(find rules -type f -name '*.md' | wc -l) files"
	@echo "Workflows:   $$(find workflows -type f -name '*.md' | wc -l) files"
	@echo "Tools:       $$(find tools -maxdepth 1 -type d | wc -l) dirs"
	@echo ""
	@echo "Total Markdown: $$(find . -type f -name '*.md' | wc -l) files"
	@echo "Total Python:   $$(find . -type f -name '*.py' | wc -l) files"

validate:
	@echo "Validating resources..."
	$(python) tools/validate-resource/validate.py

check-links:
	@echo "Checking for dead links..."
	$(python) tools/check-dead-links/check.py

check: validate check-links
	@echo ""
	@echo "All checks passed"

export:
	@mkdir -p $(export_dir)
	$(python) tools/export-skills-to-md/export.py --all --output $(export_dir)/skills-bundle.md
	@echo "Exported to $(export_dir)/skills-bundle.md"

export-prompts:
	@mkdir -p $(export_dir)
	@find prompts -name '*.md' -exec cat {} + > $(export_dir)/prompts-bundle.md
	@echo "Exported prompts to $(export_dir)/prompts-bundle.md"

export-all: export export-prompts
	@echo "All bundles created in $(export_dir)/"

sync-cursor:
	$(python) tools/sync-skills-to-cursor/sync.py --all

sync-claude:
	$(python) tools/sync-skills-to-claude/sync.py --all

sync-all: sync-cursor sync-claude
	@echo "Synced to Cursor and Claude"

install:
	pip install -r tools/requirements.txt

test:
	pip install pytest
	pytest tools/tests/ -v

clean:
	rm -rf $(export_dir)/
	rm -rf .cursor/rules/*.md
	rm -rf .claude/agents/*.md
	@echo "Cleaned exports and IDE sync artifacts"
