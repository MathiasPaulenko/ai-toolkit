# Behave API Reference

Extended reference extracted from the Behave BDD Skill. Consult this for detailed CLI flags, model objects, and advanced features.

---

## Model Objects

### Feature

```python
feature.name        # str
feature.filename    # str
feature.line        # int
feature.tags        # list[str]
feature.scenarios   # list[Scenario]
feature.background  # Background or None
```

### Scenario

```python
scenario.name       # str
scenario.tags       # list[str]
scenario.steps      # list[Step]
scenario.status     # 'passed' | 'failed' | 'skipped' | 'untested'
scenario.duration   # float (seconds)
scenario.background # Background or None (the Background steps if any)
```

### Step

```python
step.name           # str
step.keyword        # 'Given', 'When', 'Then', 'And', 'But'
step.status         # str
step.duration       # float
step.error_message  # str or None
step.table          # Table or None
step.text           # str or None
```

### Accessing Background Steps

```python
def before_scenario(context, scenario):
    if scenario.background:
        for step in scenario.background.steps:
            print(f"Background step: {step.keyword} {step.name}")
```

### Capturing Error Messages in Hooks

```python
def after_step(context, step):
    if step.status == 'failed':
        print(f"FAILED: {step.name}")
        print(f"ERROR: {step.error_message}")
        context.last_error = step.error_message
```

---

## CLI Reference

### Full Command Syntax

```bash
behave [options] [ [DIR|FILE|URL][:LINE[:LINE]*] ]+
```

### Execution Control

| Flag | Description |
|------|-------------|
| `--stop` | Stop on first failure |
| `--dry-run` | Parse without executing |
| `--verbose` | Show skipped steps |
| `--no-capture` | Show print/log output immediately |
| `--no-capture-stderr` | Show stderr immediately |
| `--no-logcapture` | Disable log capture |
| `--quiet` | Alias for `--no-capture` |
| `--show-source` | Show feature file source location |
| `--show-snippets` | Show undefined step snippets |
| `--show-timings` | Show step timings |
| `--show-skipped` | Show skipped scenarios |

### Discovery & Filtering

| Flag | Description |
|------|-------------|
| `--tags=EXPR` | Filter by tag expression |
| `--name=PATTERN` | Run scenarios matching name regex |
| `--exclude=PATTERN` | Exclude files/directories |
| `--steps-catalog` | List all available step definitions |
| `--include=PATTERN` | Include only matching files |

### Output & Reporting

| Flag | Description |
|------|-------------|
| `--format=NAME` | Output formatter |
| `--outfile=FILE` | Write output to file |
| `--junit` | Enable JUnit XML output |
| `--junit-directory=DIR` | JUnit output directory |
| `--null-device` | Suppress all output |

### Configuration Overrides

| Flag | Description |
|------|-------------|
| `-D KEY=VALUE` | Set userdata key-value pair |
| `--define KEY=VALUE` | Same as `-D` |
| `--lang=LANG` | Set Gherkin language (e.g. `es`) |
| `--lang-list` | List available languages |
| `--color` / `--no-color` | Toggle colored output |

### Line-Based Execution

```bash
behave features/login.feature:10       # Run from line 10
behave features/login.feature:10:25    # Run lines 10-25
```

---

## JSON Report Structure

```json
[
  {
    "status": "passed",
    "location": "features/login.feature:1",
    "elements": [
      {
        "type": "scenario",
        "name": "Successful login",
        "steps": [
          {
            "name": "Given I am on the login page",
            "result": {
              "status": "passed",
              "duration": 0.001
            }
          }
        ]
      }
    ]
  }
]
```

---

## behave.ini Full Reference

```ini
[behave]
format = pretty
outfiles = reports/behave.json
paths = features/
tags = not @wip and not @manual
verbose = true
stdout_capture = true
stderr_capture = true
log_capture = true
logging_level = INFO
logging_format = %(levelname)s %(name)s %(message)s
logging_datefmt = %Y-%m-%d %H:%M:%S
colors = true
show_skipped = true
show_timings = true
show_source = true
show_snippets = true
scenario_outline_annotation_schema = {name} -- {row.name} @{row.id}
```

---

## Active Tags (behave 1.2.6+)

Conditional skipping based on runtime conditions.

```python
from behave.tag_matcher import ActiveTagMatcher

active_tag_values = {
    'os': os.name,
    'browser': os.environ.get('BROWSER', 'chrome'),
}

def before_scenario(context, scenario):
    matcher = ActiveTagMatcher(active_tag_values)
    if matcher.should_exclude_with(scenario.effective_tags):
        scenario.skip("Active tag mismatch")
```

```gherkin
@use.with_os=posix
Scenario: Unix-specific test
  ...

@use.with_browser=chrome
Scenario: Chrome-specific test
  ...
```

---

## Custom Formatter Template

See `formatter-template.py` for a ready-to-customize formatter.
