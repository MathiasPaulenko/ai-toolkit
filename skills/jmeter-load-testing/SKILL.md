---
name: jmeter-load-testing
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Load and performance testing with Apache JMeter. Covers test plan design, thread groups, samplers, assertions, listeners, distributed testing, and CI/CD integration.
tags: [jmeter, load-testing, performance, stress-test, jmx, ci-cd]
role: performance-engineer
model: any
trigger: When the user mentions JMeter, load testing, performance testing, stress testing, thread groups, JMX files, or distributed load testing.
---

# JMeter Load Testing

## 1. Test Plan Structure

```
Test Plan
â”œâ”€â”€ Thread Group
â”‚   â”œâ”€â”€ HTTP Request Defaults
â”‚   â”œâ”€â”€ HTTP Cookie Manager
â”‚   â”œâ”€â”€ HTTP Header Manager
â”‚   â”œâ”€â”€ CSV Data Set Config
â”‚   â”œâ”€â”€ HTTP Request (Login)
â”‚   â”œâ”€â”€ HTTP Request (Get Data)
â”‚   â””â”€â”€ HTTP Request (Submit)
â”œâ”€â”€ View Results Tree (Debug)
â”œâ”€â”€ Summary Report
â””â”€â”€ Response Assertions
```

## 2. Thread Group Configuration

| Property | Description | Example |
|----------|-------------|---------|
| Number of Threads | Virtual users | 100 |
| Ramp-up Period | Seconds to start all threads | 60 (1 user/sec) |
| Loop Count | Iterations per thread | 10 |
| Duration | Total test duration (seconds) | 300 |
| Startup Delay | Delay before starting (seconds) | 0 |

## 3. HTTP Sampler

```xml
<!-- HTTP Request Sampler -->
<HTTPSamplerProxy>
  <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
  <stringProp name="HTTPSampler.port">443</stringProp>
  <stringProp name="HTTPSampler.protocol">https</stringProp>
  <stringProp name="HTTPSampler.path">/api/v1/users</stringProp>
  <stringProp name="HTTPSampler.method">GET</stringProp>
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="limit" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">50</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
        <boolProp name="HTTPArgument.use_equals">true</boolProp>
        <stringProp name="Argument.name">limit</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
</HTTPSamplerProxy>
```

## 4. CSV Data Set Config

```csv
# users.csv
username,password
alice,pass123
bob,pass456
charlie,pass789
```

```xml
<CSVDataSet>
  <stringProp name="filename">users.csv</stringProp>
  <stringProp name="variableNames">username,password</stringProp>
  <boolProp name="recycle">true</boolProp>
  <boolProp name="stopThread">false</boolProp>
  <stringProp name="sharingMode">All threads</stringProp>
</CSVDataSet>
```

## 5. Assertions

```xml
<!-- Response Assertion -->
<ResponseAssertion>
  <collectionProp name="testStrings">
    <stringProp name="">200</stringProp>
  </collectionProp>
  <stringProp name="custom_message">Expected 200 OK</stringProp>
  <intProp name="testType">16</intProp>  <!-- Contains -->
</ResponseAssertion>

<!-- JSON Assertion -->
<JSONPathAssertion>
  <stringProp name="JSON_PATH">$.status</stringProp>
  <stringProp name="EXPECTED_VALUE">success</stringProp>
  <boolProp name="JSONVALIDATION">true</boolProp>
</JSONPathAssertion>
```

## 6. Extractors (Correlation)

```xml
<!-- JSON Extractor for auth token -->
<JSONPostProcessor>
  <stringProp name="JSONPostProcessor.referenceNames">authToken</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.token</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
</JSONPostProcessor>

<!-- Use extracted token in subsequent request -->
<HeaderManager>
  <collectionProp name="HeaderManager.headers">
    <elementProp name="Authorization" elementType="Header">
      <stringProp name="Header.name">Authorization</stringProp>
      <stringProp name="Header.value">Bearer ${authToken}</stringProp>
    </elementProp>
  </collectionProp>
</HeaderManager>
```

## 7. Listeners and Reporting

| Listener | Purpose |
|----------|---------|
| View Results Tree | Debug individual requests |
| Summary Report | Aggregate statistics |
| Aggregate Graph | Response time distribution |
| Backend Listener | Send metrics to InfluxDB/Grafana |

### Backend Listener (InfluxDB)

```xml
<BackendListener>
  <stringProp name="classname">org.apache.jmeter.visualizers.backend.influxdb.InfluxDBBackendListenerClient</stringProp>
  <elementProp name="arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="influxdbUrl" elementType="Argument">
        <stringProp name="Argument.value">http://influxdb:8086/write?db=jmeter</stringProp>
      </elementProp>
      <elementProp name="application" elementType="Argument">
        <stringProp name="Argument.value">my-api</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
</BackendListener>
```

## 8. Distributed Testing

### Master (Controller)

```bash
jmeter -n -t test-plan.jmx -R slave1,slave2,slave3 -l results.jtl
# -n: non-GUI mode
# -t: test plan
# -R: remote servers
# -l: log file
```

### Slave (Load Generator)

```bash
# Start JMeter server on each slave
./jmeter-server -Djava.rmi.server.hostname=slave1
```

### Properties

```properties
# jmeter.properties
remote_hosts=slave1,slave2,slave3
server_port=1099
client.rmi.localport=0
```

## 9. CI/CD Integration

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Load Test') {
            steps {
                sh '''
                    jmeter -n -t api-load-test.jmx \
                           -l results.jtl \
                           -e -o dashboard
                '''
            }
        }
    }
    post {
        always {
            perfReport sourceDataFiles: 'results.jtl'
            publishHTML([
                reportDir: 'dashboard',
                reportFiles: 'index.html',
                reportName: 'JMeter Dashboard'
            ])
        }
    }
}
```

### GitHub Actions

```yaml
- name: Run JMeter Tests
  run: |
    wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.tgz
    tar -xzf apache-jmeter-5.6.3.tgz
    ./apache-jmeter-5.6.3/bin/jmeter -n -t test-plan.jmx -l results.jtl

- name: Upload Results
  uses: actions/upload-artifact@v4
  with:
    name: jmeter-results
    path: results.jtl
```

## 10. Best Practices

- Run in **non-GUI mode** for actual tests (GUI is for design only).
- Use **HTTP Cache Manager** to simulate browser caching.
- Use **HTTP Cookie Manager** for session state.
- Add **Think Time** (Gaussian Random Timer) between requests.
- Use **Throughput Controller** for mixed-load scenarios.
- Monitor server resources during tests (CPU, memory, DB connections).
- Start small (10 users) and ramp up gradually.
- Use **JSR223 PreProcessor** with Groovy for complex logic (faster than BeanShell).

## 11. JSR223 Groovy Script

```groovy
// PreProcessor: Generate dynamic payload
import groovy.json.JsonBuilder

def payload = new JsonBuilder([
    timestamp: System.currentTimeMillis(),
    userId: vars.get("userId"),
    action: "click"
]).toString()

sampler.addNonEncodedArgument("", payload, "")
sampler.setPostBodyRaw(true)
```
