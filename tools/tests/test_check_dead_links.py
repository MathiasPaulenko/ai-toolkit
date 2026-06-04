"""Tests for check-dead-links tool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "check-dead-links"))

import check as c


def test_find_urls_finds_https():
    text = "Check out https://example.com/page for details."
    urls = c.find_urls(text)
    assert "https://example.com/page" in urls


def test_find_urls_finds_http():
    text = "See http://old.example.com/docs"
    urls = c.find_urls(text)
    assert "http://old.example.com/docs" in urls


def test_find_urls_no_urls():
    text = "This has no links at all."
    urls = c.find_urls(text)
    assert len(urls) == 0


def test_should_ignore_localhost():
    assert c.should_ignore("http://localhost:8080", ["localhost", "127.0.0.1"])


def test_should_ignore_not_matching():
    assert not c.should_ignore("https://example.com", ["localhost"])
