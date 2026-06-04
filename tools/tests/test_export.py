"""Tests for export-skills-to-md tool."""

import sys
from pathlib import Path

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "export-skills-to-md"))

import export as e


def test_build_bundle_includes_title():
    skills = []
    bundle = e.build_bundle(skills, title="Test Bundle")
    assert "# Test Bundle" in bundle


def test_build_bundle_empty_skills():
    bundle = e.build_bundle([], title="Empty")
    assert "# Empty" in bundle
    assert "Generated on" in bundle


def test_build_bundle_with_mock_skill(tmp_path):
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# Test Skill\n\nContent here.\n")

    bundle = e.build_bundle([skill_dir], title="Test")
    assert "## Skill: test-skill" in bundle
    assert "# Test Skill" in bundle
    assert "Content here." in bundle
