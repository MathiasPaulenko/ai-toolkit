---
name: CI Visual Regression Workflow
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Set up visual regression testing with wavexis in GitHub Actions. Covers baseline capture, storage, PR comparison, threshold tuning, artifact upload, and baseline updates on merge."
tags: [visual-regression, ci-cd, github-actions, wavexis]
role: test-architect
---

# CI Visual Regression Workflow

Set up visual regression testing with wavexis in GitHub Actions. Capture baselines, compare on every PR, fail on visual differences, and update baselines on merge.

## Prerequisites

- [ ] Python 3.11+ installed
- [ ] `pip install wavexis`
- [ ] Chrome 112+ installed (for headless screenshots)
- [ ] Target application accessible (staging URL)
- [ ] GitHub repository with Actions enabled

## Phase 1: Capture Baseline Screenshots

### Step 1: Define Pages to Capture

Create a baseline manifest listing all pages and viewports:

```yaml
# baselines/manifest.yml
pages:
  - name: home
    url: https://staging.example.com/
    viewport:
      width: 1440
      height: 900
    full_page: true
  - name: login
    url: https://staging.example.com/login
    viewport:
      width: 1440
      height: 900
    full_page: true
  - name: product-list
    url: https://staging.example.com/products
    viewport:
      width: 1440
      height: 900
    full_page: true
  - name: product-detail
    url: https://staging.example.com/products/widget
    viewport:
      width: 1440
      height: 900
    full_page: true
  - name: cart
    url: https://staging.example.com/cart
    viewport:
      width: 1440
      height: 900
    full_page: true
  - name: mobile-home
    url: https://staging.example.com/
    viewport:
      width: 390
      height: 844
    full_page: true
```

### Step 2: Capture Baselines

```bash
# Capture all baselines from manifest
wavexis screenshot --manifest baselines/manifest.yml --output baselines/

# Or capture individual pages
wavexis screenshot https://staging.example.com/ \
  --output baselines/home.png \
  --viewport 1440x900 \
  --full-page

wavexis screenshot https://staging.example.com/login \
  --output baselines/login.png \
  --viewport 1440x900 \
  --full-page
```

### Step 3: Verify Baselines

```bash
# List captured baselines
ls -la baselines/

# Verify baseline integrity
wavexis visual-diff --baseline baselines/ --check-only
```

## Phase 2: Store Baselines

### Option A: Repository Storage (Recommended for Small Projects)

```text
baselines/
  manifest.yml
  home.png
  login.png
  product-list.png
  product-detail.png
  cart.png
  mobile-home.png
```

Commit baselines to the repository:

```bash
git add baselines/
git commit -m "chore: add visual regression baselines"
```

### Option B: Artifact Storage (Recommended for Large Projects)

Store baselines as GitHub Actions artifacts or in cloud storage (S3, GCS):

```bash
# Upload baselines to S3
aws s3 sync baselines/ s3://my-bucket/visual-baselines/

# Download baselines in CI
aws s3 sync s3://my-bucket/visual-baselines/ baselines/
```

## Phase 3: Add GitHub Actions Workflow

### Step 1: Create the Workflow File

```yaml
# .github/workflows/visual-regression.yml
name: Visual Regression

on:
  pull_request:
    paths:
      - "src/**"
      - "public/**"
      - "baselines/**"

jobs:
  visual-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install wavexis
        run: pip install wavexis

      - name: Install Chrome
        run: |
          wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
          sudo dpkg -i google-chrome-stable_current_amd64.deb

      - name: Capture current screenshots
        run: |
          wavexis screenshot --manifest baselines/manifest.yml \
            --output current/ \
            --headless

      - name: Compare with baselines
        id: diff
        run: |
          wavexis visual-diff \
            --baseline baselines/ \
            --current current/ \
            --output diff/ \
            --threshold 0.01 \
            --fail-on-diff
        continue-on-error: true

      - name: Upload diff images
        if: steps.diff.outcome == 'failure'
        uses: actions/upload-artifact@v4
        with:
          name: visual-diff
          path: |
            diff/
            current/
          retention-days: 30

      - name: Fail PR if visual differences detected
        if: steps.diff.outcome == 'failure'
        run: |
          echo "::error::Visual differences detected. Review the diff artifacts."
          exit 1
```

### Step 2: Configure Threshold

The `--threshold` parameter controls the sensitivity:

| Threshold | Sensitivity | Use Case |
|-----------|-------------|----------|
| `0.001` | Very high | Pixel-perfect design systems |
| `0.01` | High | Most web applications |
| `0.05` | Medium | Applications with dynamic content |
| `0.10` | Low | Early-stage projects with frequent changes |

### Step 3: Add Path Filtering (Optional)

To avoid running visual regression on non-visual changes:

```yaml
on:
  pull_request:
    paths:
      - "src/**"
      - "public/**"
      - "baselines/**"
      - ".github/workflows/visual-regression.yml"
```

## Phase 4: Compare Current Screenshots with Baselines

### Step 1: Run Comparison Locally

```bash
# Capture current screenshots
wavexis screenshot --manifest baselines/manifest.yml --output current/ --headless

# Compare
wavexis visual-diff \
  --baseline baselines/ \
  --current current/ \
  --output diff/ \
  --threshold 0.01
```

### Step 2: Review Diff Output

```text
diff/
  home.diff.png          # Visual diff overlay
  home.diff.json         # Diff metadata (pixels changed, percentage)
  login.diff.png
  login.diff.json
  ...
```

### Step 3: Interpret Diff Results

```json
{
  "page": "home",
  "baseline": "baselines/home.png",
  "current": "current/home.png",
  "pixels_changed": 1523,
  "total_pixels": 1296000,
  "percentage": 0.00117,
  "threshold": 0.01,
  "passed": true
}
```

### Step 4: Ignore Dynamic Regions (Optional)

For pages with dynamic content (timestamps, ads, user-generated content), create ignore regions:

```yaml
# baselines/ignore-regions.yml
home:
  - selector: ".timestamp"
    reason: "Dynamic timestamp"
  - selector: ".ad-banner"
    reason: "Third-party ad content"
login:
  - selector: ".captcha"
    reason: "Dynamic captcha image"
```

```bash
wavexis visual-diff \
  --baseline baselines/ \
  --current current/ \
  --output diff/ \
  --threshold 0.01 \
  --ignore-regions baselines/ignore-regions.yml
```

## Phase 5: Fail PR if Visual Differences Exceed Threshold

### Step 1: CI Gate Behavior

| Outcome | CI Action | PR Status |
|---------|-----------|-----------|
| No differences | Pass | Green check |
| Differences within threshold | Pass | Green check |
| Differences exceed threshold | Fail | Red X |
| Error (missing baseline) | Fail | Red X |

### Step 2: Add PR Comment (Optional)

```yaml
      - name: Comment on PR
        if: steps.diff.outcome == 'failure'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const diffs = fs.readdirSync('diff/').filter(f => f.endsWith('.diff.json'));
            const results = diffs.map(f => {
              const data = JSON.parse(fs.readFileSync(`diff/${f}`));
              return `- **${data.page}**: ${data.percentage * 100}% changed (${data.pixels_changed} pixels)`;
            });
            github.rest.issues.createComment({
              ...context.repo,
              issue_number: context.issue.number,
              body: `### Visual Regression Results\n\n${results.join('\n')}\n\nReview the [diff artifacts](${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}) for details.`
            });
```

## Phase 6: Upload Diff Images as Artifacts

### Step 1: Upload in Workflow

```yaml
      - name: Upload diff artifacts
        if: steps.diff.outcome == 'failure'
        uses: actions/upload-artifact@v4
        with:
          name: visual-diff-${{ github.event.pull_request.number }}
          path: |
            diff/
            current/
            baselines/
          retention-days: 30
```

### Step 2: Download and Review

Contributors download the artifact from the PR check page:

1. Go to the PR Checks tab
2. Click on the "Visual Regression" workflow
3. Download the `visual-diff-<PR-number>` artifact
4. Open the `.diff.png` files to review visual changes

## Phase 7: Update Baselines on Merge to Main

### Step 1: Create Baseline Update Workflow

```yaml
# .github/workflows/update-baselines.yml
name: Update Visual Baselines

on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "public/**"

jobs:
  update-baselines:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install wavexis
        run: pip install wavexis

      - name: Install Chrome
        run: |
          wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
          sudo dpkg -i google-chrome-stable_current_amd64.deb

      - name: Capture new baselines
        run: |
          wavexis screenshot --manifest baselines/manifest.yml \
            --output baselines/ \
            --headless

      - name: Commit updated baselines
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add baselines/
          git diff --staged --quiet || git commit -m "chore: update visual regression baselines"
          git push
```

### Step 2: Manual Baseline Update (Alternative)

```bash
# Capture new baselines locally
wavexis screenshot --manifest baselines/manifest.yml --output baselines/ --headless

# Commit and push
git add baselines/
git commit -m "chore: update visual regression baselines"
git push
```

## Checklist

- [ ] Baseline manifest created (`baselines/manifest.yml`)
- [ ] Baseline screenshots captured
- [ ] Baselines committed to repository or artifact storage
- [ ] GitHub Actions workflow created (`.github/workflows/visual-regression.yml`)
- [ ] Threshold configured (`--threshold 0.01` or appropriate value)
- [ ] Path filtering configured (optional)
- [ ] Ignore regions configured for dynamic content (optional)
- [ ] Diff artifacts uploaded on failure
- [ ] PR comment automation added (optional)
- [ ] Baseline update workflow created (`.github/workflows/update-baselines.yml`)
- [ ] Team trained on reviewing diff artifacts
