---
name: Octane ALM
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Micro Focus ALM Octane integration guide. Covers REST API, entity management, defect tracking, test automation integration, and CI/CD pipeline reporting.
tags: [octane, alm, testing, defect-management, rest-api, ci-cd]
role: qa-engineer
model: any
trigger: When the user mentions Octane, ALM, Micro Focus, defect management, test management, or ALM integration.
---

# Octane ALM

## 1. REST API Basics

### Authentication

```bash
# Using client_id and client_secret
curl -X POST https://octane.example.com/authentication/sign_in \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
  }'
# Response: { "access_token": "...", "token_type": "jwt", "expires_in": 3600 }
```

### Common Endpoints

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Defects | `/api/shared_spaces/{space_id}/workspaces/{ws_id}/defects` | GET, POST, PUT |
| Tests | `/api/shared_spaces/{space_id}/workspaces/{ws_id}/tests` | GET, POST |
| Runs | `/api/shared_spaces/{space_id}/workspaces/{ws_id}/runs` | GET, POST |
| Requirements | `/api/shared_spaces/{space_id}/workspaces/{ws_id}/requirements` | GET, POST |
| Users | `/api/shared_spaces/{space_id}/workspaces/{ws_id}/workspace_users` | GET |

### Fetch Defects

```bash
curl -X GET "https://octane.example.com/api/shared_spaces/1001/workspaces/1002/defects?query=%22severity%20EQ%20%5C%221%5C%22%22" \
  -H "Authorization: jwt $TOKEN"
```

## 2. Python Integration

```python
import requests

class OctaneClient:
    def __init__(self, base_url, client_id, client_secret, space_id, workspace_id):
        self.base_url = base_url.rstrip('/')
        self.space_id = space_id
        self.workspace_id = workspace_id
        self.session = requests.Session()
        self._authenticate(client_id, client_secret)

    def _authenticate(self, client_id, client_secret):
        resp = self.session.post(
            f"{self.base_url}/authentication/sign_in",
            json={"client_id": client_id, "client_secret": client_secret}
        )
        resp.raise_for_status()
        token = resp.json()["access_token"]
        self.session.headers.update({"Authorization": f"jwt {token}"})

    def get_defects(self, query=None, limit=100):
        params = {"limit": limit}
        if query:
            params["query"] = f'"{query}"'
        return self.session.get(
            f"{self.base_url}/api/shared_spaces/{self.space_id}/workspaces/{self.workspace_id}/defects",
            params=params
        ).json()

    def create_defect(self, name, severity, owner_email):
        payload = {
            "name": name,
            "severity": {"id": severity},
            "phase": {"id": "phase.defect.new"},
            "owner": {"type": "workspace_user", "email": owner_email},
        }
        return self.session.post(
            f"{self.base_url}/api/shared_spaces/{self.space_id}/workspaces/{self.workspace_id}/defects",
            json=payload
        ).json()

    def update_run_result(self, run_id, status):
        payload = {
            "id": run_id,
            "status": {"id": f"list_node.run_status.{status}"}
        }
        return self.session.put(
            f"{self.base_url}/api/shared_spaces/{self.space_id}/workspaces/{self.workspace_id}/runs/{run_id}",
            json=payload
        ).json()
```

## 3. Entity Types and Fields

| Entity | Common Fields |
|--------|--------------|
| Defect | name, severity, priority, phase, owner, detected_in_release, description, story_points |
| Test | name, test_type, phase, owner, description, steps, covered_requirements |
| Run | name, status, duration, native_status, started, ended, test, test_run |
| Requirement | name, phase, author, description, covered_by_tests, story_points |

### Severity Levels

| ID | Name |
|----|------|
| 1 | Critical |
| 2 | High |
| 3 | Medium |
| 4 | Low |

### Status Values

| Entity | Status |
|--------|--------|
| Defect | new, open, fixed, closed, rejected, reopened |
| Test | draft, ready, obsolete |
| Run | passed, failed, blocked, skipped, not_completed |

## 4. Defect Management Workflow

```
New → Open → Fixed → Closed
  |      |
  +----> Reopened
```

### Automated Defect Creation from CI

```python
def report_test_failure(test_name, error_msg, build_id):
    client = OctaneClient(...)
    defect = client.create_defect(
        name=f"[Build {build_id}] {test_name} failed",
        severity=2,  # High
        owner_email="qa-lead@example.com"
    )
    # Add comment with stack trace
    client.session.post(
        f"{client.base_url}/api/shared_spaces/{client.space_id}/workspaces/{client.workspace_id}/comments",
        json={
            "text": error_msg,
            "owner_work_item": {"type": "defect", "id": defect["id"]}
        }
    )
    return defect["id"]
```

## 5. Test Automation Integration

### Upload Test Results

```python
def upload_junit_results(xml_path, release_id, pipeline_name):
    client = OctaneClient(...)
    
    # Parse JUnit XML
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    for testcase in root.iter('testcase'):
        test_name = testcase.get('name')
        duration = int(float(testcase.get('time', 0)) * 1000)
        
        status = 'passed'
        if testcase.find('failure') is not None:
            status = 'failed'
        elif testcase.find('skipped') is not None:
            status = 'skipped'
        
        # Create run
        payload = {
            "name": test_name,
            "status": {"id": f"list_node.run_status.{status}"},
            "duration": duration,
            "test": {"type": "test_manual", "name": test_name},
            "release": {"type": "release", "id": release_id},
            "pipeline": pipeline_name,
        }
        client.session.post(
            f"{client.base_url}/api/shared_spaces/{client.space_id}/workspaces/{client.workspace_id}/runs",
            json=payload
        )
```

## 6. CI/CD Pipeline Reporting

### GitLab CI Integration

```yaml
report-octane:
  stage: report
  script:
    - pip install requests
    - python report_to_octane.py --build-id $CI_PIPELINE_ID --results results.xml
  only:
    - merge_requests
    - main
```

```python
# report_to_octane.py
import argparse
from octane_client import OctaneClient

parser = argparse.ArgumentParser()
parser.add_argument("--build-id")
parser.add_argument("--results")
args = parser.parse_args()

client = OctaneClient.from_env()
upload_junit_results(args.results, release_id="release_2024_1", pipeline_name=args.build_id)
```

## 7. Dashboards and Reporting

- Use **OCTANE widgets** for real-time dashboards.
- Track **defect aging** by phase.
- Monitor **test coverage** by requirement.
- Measure **automation ratio** (automated vs manual runs).
- Generate **pipeline health** reports.

## 8. Best Practices

- Use dedicated API users with minimal permissions.
- Cache access tokens; refresh before expiry.
- Use query parameters to limit result sets.
- Handle pagination with `offset` and `limit`.
- Log all API calls for audit trails.
- Map Octane defects to source control commits for traceability.
- Use custom fields for project-specific metadata.
