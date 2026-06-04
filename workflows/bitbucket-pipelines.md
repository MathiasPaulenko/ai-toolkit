---
name: Bitbucket Pipelines
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Bitbucket Pipelines CI/CD workflow. Covers pipeline configuration, deployment steps, branch strategies, caches, and integrations.
tags: [workflow, bitbucket, ci-cd, pipeline, deployment, branches]
role: devops-engineer
---

# Bitbucket Pipelines

## 1. Basic Configuration

```yaml
# bitbucket-pipelines.yml
image: python:3.11

pipelines:
  default:
    - step:
        name: Lint and Test
        caches:
          - pip
        script:
          - pip install -r requirements.txt
          - flake8 src/
          - pytest tests/ --cov=src
```

## 2. Branch Strategies

### Feature Branches

```yaml
pipelines:
  branches:
    feature/*:
      - step:
          name: Test
          caches:
            - pip
          script:
            - pytest tests/
```

### Pull Requests

```yaml
pipelines:
  pull-requests:
    feature/*:
      - step:
          name: PR Checks
          caches:
            - pip
          script:
            - pytest tests/
            - bandit -r src/
```

### Main Branch

```yaml
pipelines:
  branches:
    main:
      - step:
          name: Build
          script:
            - docker build -t $DOCKER_IMAGE:latest .
      - step:
          name: Deploy to Production
          trigger: manual
          deployment: production
          script:
            - ./deploy.sh production
```

## 3. Caches

| Cache | Purpose |
|-------|---------|
| `pip` | Python dependencies |
| `npm` | Node.js dependencies |
| `maven` | Maven dependencies |
| `gradle` | Gradle dependencies |
| `composer` | PHP dependencies |
| `docker` | Docker layers |

```yaml
caches:
  pip:
    key:
      files:
        - requirements.txt
    path: ~/.cache/pip
```

## 4. Services

```yaml
- step:
    name: Integration Tests
    services:
      - postgres
      - redis
    caches:
      - pip
    script:
      - pytest tests/integration/

definitions:
  services:
    postgres:
      image: postgres:16
      variables:
        POSTGRES_DB: testdb
        POSTGRES_USER: testuser
        POSTGRES_PASSWORD: testpass
    redis:
      image: redis:7
```

## 5. Deployments

```yaml
pipelines:
  branches:
    develop:
      - step:
          name: Deploy to Staging
          deployment: staging
          script:
            - pipe: atlassian/aws-elasticbeanstalk-deploy:1.1.0
              variables:
                AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
                AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY
                AWS_DEFAULT_REGION: "us-east-1"
                APPLICATION_NAME: "my-app"
                ENVIRONMENT_NAME: "staging"
                ZIP_FILE: "build.zip"

    main:
      - step:
          name: Deploy to Production
          deployment: production
          trigger: manual
          script:
            - pipe: atlassian/aws-elasticbeanstalk-deploy:1.1.0
              variables:
                APPLICATION_NAME: "my-app"
                ENVIRONMENT_NAME: "production"
                ZIP_FILE: "build.zip"
```

## 6. Custom Pipes

```yaml
- step:
    name: Deploy with Custom Pipe
    script:
      - pipe: docker://myregistry/my-pipe:1.0.0
        variables:
          API_KEY: $API_KEY
          TARGET_ENV: "production"
```

## 7. Artifacts

```yaml
- step:
    name: Build
    script:
      - ./build.sh
    artifacts:
      - build/**
      - coverage/**
```

## 8. Parallel Steps

```yaml
- step:
    name: Unit Tests
    parallel:
      - step:
          name: Python 3.9
          image: python:3.9
          script:
            - pytest
      - step:
          name: Python 3.10
          image: python:3.10
          script:
            - pytest
      - step:
          name: Python 3.11
          image: python:3.11
          script:
            - pytest
```

## 9. Workspace Variables

Configure in Repository Settings > Pipelines > Repository variables:

| Variable | Purpose |
|----------|---------|
| `DOCKER_USERNAME` | Registry username |
| `DOCKER_PASSWORD` | Registry password |
| `AWS_ACCESS_KEY_ID` | AWS credentials |
| `SONAR_TOKEN` | SonarQube token |
| `SLACK_WEBHOOK` | Notifications |
