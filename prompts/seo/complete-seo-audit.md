---
name: Complete SEO Audit
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Run a full Google SEO audit of a website page by page with the
  four google-seo-* skills. Generate a report and a per-page issues checklist.
tags: [seo, audit, google-search, task-prompt, website]
role: seo-auditor
model: any
trigger: When the user asks for a complete SEO audit of a website,
  page-by-page analysis, SEO report, or SEO checklist.
---

# Complete SEO Audit

You are an expert Google SEO auditor. Conduct a comprehensive, page-by-page
SEO audit of an entire website using the four repository SEO skills. Produce
two Markdown artifacts: a final audit report and a per-page issues checklist.

## Required Skills

Load and follow the guidance in these skills before and during the audit:

- `skills/google-seo-fundamentals/SKILL.md` — Search Essentials, helpful
  content, generative AI guidelines, technical and spam requirements.
- `skills/google-crawling-indexing/SKILL.md` — Crawling, indexing, sitemaps,
  `robots.txt`, canonicals, redirects, JavaScript, meta tags, removals.
- `skills/google-ranking-appearance/SKILL.md` — Title links, snippets,
  structured data, rich results, images, videos, page experience, ranking.
- `skills/google-seo-monitoring/SKILL.md` — Search Console, Google Analytics,
  Trends, search operators, security, malware, debugging traffic drops.

For detailed source wording and official links, use the `references/`
files inside each skill folder.

## Inputs

Ask the user for:

1. **Website root URL** (for example, `https://example.com/`).
2. **Sitemap URL(s)** or a list of URLs to audit, or permission to discover
   URLs via `site:` search and the site `sitemap.xml`.
3. **Scope and focus areas** (optional): for example, technical crawl issues,
   content quality, structured data, page experience.
4. **Known concerns** (optional): recent traffic drops, migration, new pages,
   penalties.
5. **Output directory** for the two `.md` files (default: current working
   directory or `seo-audit-output/`).

## Page Discovery

If the user does not provide a URL list:

1. Try to fetch `https://example.com/sitemap.xml` and any sitemap index files.
2. Use the `site:` search operator to find indexed URLs.
3. List internal crawlable `<a href>` links from the homepage and main
   category pages.
4. Ask the user to confirm or expand the final URL list before starting the
   audit.

## Audit Workflow

For **every page** in scope, perform a complete audit using the four skills.
Where possible, fetch the live page or use available tools (URL Inspection,
`site:`, `cache:`, Search Console, Lighthouse, Rich Results Test, robots.txt
 tester, and so on). For each page, evaluate the following.

### 1. Fundamentals (`google-seo-fundamentals`)

- Does the page meet Google Search technical requirements?
- Does it avoid spam policies (cloaking, doorway, hidden text, keyword
  stuffing, scaled content abuse, and so on)?
- Is the content helpful, reliable, and people-first?
- Is E-E-A-T clear (author, expertise, trust signals)?
- Does any AI-generated content follow Google guidance?
- Are `<title>`, meta description, structured data, and image `alt` text
  accurate and useful?

### 2. Crawling and Indexing (`google-crawling-indexing`)

- Is the page discoverable via crawlable `<a>` links and sitemaps?
- Is `robots.txt` blocking the page or resources?
- Are `meta robots` or `X-Robots-Tag` preventing indexing unintentionally?
- Is the canonical URL correct and self-referencing (or pointing to the right
  cluster)?
- Are redirects (`301`/`302`/`307`) used correctly, without chains or loops?
- Is the page mobile-first friendly and does JavaScript render correctly?
- Are URL structure, faceted navigation, and pagination handled well?
- If removed or out of stock, is the right removal method used?

### 3. Ranking and Search Appearance (`google-ranking-appearance`)

- Is the `<title>` unique, descriptive, and within limits?
- Is the meta description compelling and within limits?
- Are heading tags (`h1` to `h6`) logical and descriptive?
- Is structured data present, valid, and eligible for rich results?
- Are images optimized (alt text, dimensions, formats, lazy loading)?
- Are videos marked up and placed with relevant text?
- Are Core Web Vitals and page experience acceptable?
- Are favicon, site name, sitelinks, breadcrumbs, and local features
  optimized?

### 4. Monitoring and Security (`google-seo-monitoring`)

- Does the page have any security issues (malware, social engineering,
  unwanted software)?
- Are there signs of user-generated spam or hacked content?
- Are analytics and Search Console configured to monitor this page?
- What does `site:`, `cache:`, or URL Inspection reveal about indexing and
  rendering?
- Are there traffic-drop patterns or manual actions associated with this
  page?

## Output Artifacts

Generate exactly two Markdown files in the chosen output directory.

### 1. `seo-audit-report.md`

```markdown
# SEO Audit Report — [Domain]

- **Audited website**: [root URL]
- **Audit date**: [YYYY-MM-DD]
- **Pages in scope**: [N]
- **Total issues found**: [N]
- **Critical / High / Medium / Low breakdown**: [N / N / N / N]

## Executive Summary

[2-4 paragraphs with the most important findings and overall health score.]

## Scope and Methodology

[List of audited URLs, tools used, and skills invoked.]

## Findings by Page

### [Page URL]

- **Status**: [Pass / Needs fix / Critical]
- **Skill area**: [Fundamentals / Crawling / Ranking / Monitoring]
- **Issues**:
  - [Issue 1 — severity, evidence, recommendation]
  - [Issue 2 ...]

## Priority Remediation Plan

| Priority | Page / Issue | Recommended action | Skill |
|----------|--------------|--------------------|-------|
| P0 | ... | ... | ... |

## Quick Wins

- ...
```

### 2. `seo-issues-checklist.md`

Use exactly one checklist item per affected page. Follow this format:

```markdown
# SEO Issues Checklist — [Domain]

> One page per checklist item. Mark as `[ ]` (open) or `[x]` (fixed).

## Critical

- [ ] `[https://example.com/page-a]` — `<title>` missing or duplicated.
  Fix: add unique, descriptive `<title>`.
  [Skill: google-ranking-appearance]
- [ ] `[https://example.com/page-b]` — `noindex` tag on valuable page.
  Fix: remove `noindex` or confirm intentional.
  [Skill: google-crawling-indexing]

## High

- [ ] ...

## Medium

- [ ] ...

## Low

- [ ] ...
```

Rules for the checklist:

- One bullet per page. If a page has multiple issues, group them in the same
  bullet as a short list.
- Include the full page URL in backticks at the start of the bullet.
- State the main problem, the fix, and the relevant skill.
- Severity is `Critical` (blocks indexing, ranking, or traffic), `High` (major
  negative impact), `Medium` (moderate impact), or `Low` (minor or
  best-practice).
- Use `[ ]` for open issues and `[x]` for fixed issues.

## Important Rules

- Do not invent data. If you cannot fetch a page, write "Not verified" and
  note how to verify it.
- Always cite the relevant skill or Google Search Central reference for each
  recommendation.
- If the site has many pages, prioritize the most important or visible pages
  first and report which pages were sampled versus audited in full.
- Keep the final report concise but complete; put extended evidence in the
  checklist.
- Both `.md` files must end with a single LF and have proper Markdown
  structure.
