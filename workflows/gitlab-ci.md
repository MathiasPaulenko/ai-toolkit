---
name: GitLab CI
version: 1.0.0
author: Mathias Paulenko Echeverz
description: GitLab CI/CD pipeline creation workflow. Covers stages, jobs, runners, artifacts, caching, environments, and deployment strategies.
tags: [workflow, gitlab, ci-cd, pipeline, runner, deployment]
role: devops-engineer
---

# GitLab CI

## 1. Pipeline Structure

```yaml
stages:
  - build
  - test
  - security
  - package
  - deploy
  - cleanup
```

## 2. Basic Jobs

### Build Stage

```yaml
build-java:
  stage: build
  image: eclipse-temurin:21-jdk
  script:
    - ./mvnw compile -DskipTests
  artifacts:
    paths:
      - target/classes
    expire_in: 1 hour
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .m2/repository
```

### Test Stage

```yaml
test-unit:
  stage: test
  image: eclipse-temurin:21-jdk
  script:
    - ./mvnw test
  artifacts:
    reports:
      junit: target/surefire-reports/TEST-*.xml
    paths:
      - target/site/jacoco/
  coverage: '/Total.*?([0-9]{1,3})%/'  # Extract from output

test-integration:
  stage: test
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### Security Stage

```yaml
sonarqube:
  stage: security
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner
      -Dsonar.projectKey=$CI_PROJECT_PATH
      -Dsonar.sources=src
      -Dsonar.host.url=$SONAR_URL
      -Dsonar.login=$SONAR_TOKEN
```

## 3. Runners

### Shared Runners (GitLab.com)

Already configured. Use tags to select:

```yaml
tags:
  - docker
  - linux
  - amd64
```

### Self-Managed Runner

```bash
# Register runner
gitlab-runner register \
  --url https://gitlab.com \
  --registration-token REGISTRATION_TOKEN \
  --executor docker \
  --docker-image docker:24 \
  --description "Docker Runner"
```

## 4. Caching and Artifacts

| Feature | Purpose | Scope |
|---------|---------|-------|
| `cache` | Reuse dependencies between pipelines | Global / Branch / Job |
| `artifacts` | Pass files between jobs | Pipeline |

```yaml
cache:
  key:
    files:
      - pom.xml
  paths:
    - .m2/repository
  policy: pull-push

artifacts:
  name: "$CI_JOB_NAME-$CI_COMMIT_REF_NAME"
  paths:
    - target/*.jar
  expire_in: 1 week
```

## 5. Environments and Deployment

```yaml
deploy-staging:
  stage: deploy
  script:
    - kubectl config use-context staging
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-prod:
  stage: deploy
  script:
    - kubectl config use-context production
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  environment:
    name: production
    url: https://app.example.com
  when: manual  # Require button click
  only:
    - main
```

## 6. Templates and Includes

```yaml
# .gitlab/ci/common.yml
.common-script:
  before_script:
    - echo "Running common setup"
    - apt-get update && apt-get install -y curl

# .gitlab-ci.yml
include:
  - local: ".gitlab/ci/common.yml"

build:
  extends: .common-script
  stage: build
  script:
    - ./build.sh
```

## 7. Parallel Jobs and Matrix

```yaml
test:matrix:
  stage: test
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.9", "3.10", "3.11"]
        OS: ["ubuntu", "alpine"]
  image: python:${PYTHON_VERSION}-${OS}
  script:
    - pip install -r requirements.txt
    - pytest
```

## 8. Variables

```yaml
variables:
  MAVEN_OPTS: "-Dmaven.repo.local=.m2/repository"
  DOCKER_DRIVER: overlay2

job:
  variables:
    DEPLOY_ENV: "staging"
  script:
    - echo "Deploying to $DEPLOY_ENV"
```

## 9. Pipeline Triggers

```yaml
# Scheduled pipeline
pipeline-schedule:
  only:
    - schedules
  script:
    - ./run-nightly-tests.sh

# Merge request pipeline
pipeline-mr:
  only:
    - merge_requests
  script:
    - ./run-pr-checks.sh
```
