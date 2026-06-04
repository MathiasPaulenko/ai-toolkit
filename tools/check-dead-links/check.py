#!/usr/bin/env python3
"""
check-dead-links: Scans all .md files for broken external URLs.

Uses HEAD requests to check link status without downloading content.

Usage:
    python check.py                    # Check entire repo
    python check.py docs/              # Check specific directory
    python check.py --timeout 10       # Custom timeout
    python check.py --ignore localhost  # Skip patterns
"""

import argparse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import urllib.request

REPO_ROOT = Path(__file__).resolve().parents[2]
URL_PATTERN = re.compile(r"https?://[^\s\)\]\>\"]+")


def find_urls(text: str) -> set[str]:
    raw = URL_PATTERN.findall(text)
    cleaned = []
    for url in raw:
        # Strip trailing punctuation that isn't part of the URL
        url = url.rstrip(";,.>\"'<")
        cleaned.append(url)
    return set(cleaned)


def check_url(url: str, timeout: int = 10) -> tuple[bool, int | None]:
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "Mozilla/5.0 (ai-toolkit link checker)")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, resp.getcode()
    except urllib.error.HTTPError as e:
        # 403 may be blocked by bot protection; treat as OK-ish
        if e.code == 403:
            return True, 403
        return False, e.code
    except Exception:
        return False, None


def should_ignore(url: str, ignore_patterns: list[str]) -> bool:
    # Skip template variables like {location}, {id}
    if "{" in url or "}" in url:
        return True
    parsed = urlparse(url)
    for pattern in ignore_patterns:
        if pattern in parsed.netloc or pattern in url:
            return True
    return False


def scan_directory(
    directory: Path, ignore: list[str], timeout: int
) -> dict[str, list[str]]:
    dead: dict[str, list[str]] = {}
    md_files = list(directory.rglob("*.md"))

    # Collect all unique URLs to check
    url_to_files: dict[str, list[Path]] = {}
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        urls = find_urls(text)
        for url in urls:
            if should_ignore(url, ignore):
                continue
            url_to_files.setdefault(url, []).append(md_file)

    # Check URLs concurrently
    results: dict[str, tuple[bool, int | None]] = {}
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(check_url, url, timeout): url for url in url_to_files
        }
        for future in as_completed(futures):
            url = futures[future]
            try:
                results[url] = future.result()
            except Exception:
                results[url] = (False, None)

    # Aggregate failures
    for url, (ok, code) in results.items():
        if not ok:
            key = f"{url} (HTTP {code})" if code else url
            for md_file in url_to_files[url]:
                dead.setdefault(str(md_file.relative_to(REPO_ROOT)), []).append(key)

    return dead


def main():
    parser = argparse.ArgumentParser(
        description="Check for dead external links in markdown"
    )
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    parser.add_argument(
        "--timeout", type=int, default=10, help="Request timeout in seconds"
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[
            "localhost",
            "127.0.0.1",
            "example.com",
            "example.org",
            "prometheus:",
            "influxdb:",
            "grafana:",
            "jenkins:",
            "jira:",
            "soap.sforce.com",
            "github.com/org/",
            "qameta.io",
            "app",
            "weather.com",
        ],
        help="URL patterns to ignore",
    )
    args = parser.parse_args()

    target = REPO_ROOT / args.path
    if not target.exists():
        print(f"Path not found: {target}")
        return 1

    print(f"Scanning {target.relative_to(REPO_ROOT)} for dead links...\n")
    dead = scan_directory(target, args.ignore, args.timeout)

    if not dead:
        print("✅ No dead links found.")
        return 0

    total = 0
    for file, urls in dead.items():
        print(f"❌ {file}")
        for u in urls:
            print(f"   - {u}")
            total += 1

    print(f"\n❌ Found {total} dead link(s) in {len(dead)} file(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
