---
name: Testcontainers
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Integration testing with Testcontainers: PostgreSQL, Redis, Kafka, RabbitMQ, localstack. Spin up real dependencies in Docker for reliable integration tests."
tags: [integration-testing, testcontainers, docker, databases, kafka]
role: qa-engineer
model: any
trigger: When the user asks about integration testing, Testcontainers, testing with real databases, or Docker-based test dependencies.
---

# Testcontainers

Integration testing with real dependencies via Docker containers.

## 1. Why Testcontainers

| Problem | Testcontainers Solution |
|---------|------------------------|
| In-memory DB ≠ production | Real PostgreSQL, Redis, MongoDB in Docker |
| H2 dialect differences | Same engine as production |
| Kafka mocks are incomplete | Real Kafka broker + topics |
| AWS testing is hard | Localstack S3, SQS, DynamoDB |
| Test isolation | Fresh container per test class / JVM |

## 2. Quick Start (Java + JUnit 5)

```xml
<!-- pom.xml -->
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>junit-jupiter</artifactId>
  <version>1.19.0</version>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>postgresql</artifactId>
  <version>1.19.0</version>
  <scope>test</scope>
</dependency>
```

```java
@Testcontainers
public class OrderRepositoryTest {

  @Container
  static PostgreSQLContainer<?> postgres =
    new PostgreSQLContainer<>("postgres:15-alpine")
      .withDatabaseName("orders")
      .withUsername("test")
      .withPassword("test");

  @DynamicPropertySource
  static void props(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
  }

  @Autowired OrderRepository repo;

  @Test
  void shouldSaveAndFindOrder() {
    Order order = new Order("ORD-001", BigDecimal.valueOf(99.99));
    repo.save(order);
    assertThat(repo.findById("ORD-001")).isPresent();
  }
}
```

## 3. Container Types & Patterns

### PostgreSQL
```java
@Container
static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:15")
  .withInitScript("schema.sql");  // Runs on startup
```

### Redis
```java
@Container
static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
  .withExposedPorts(6379);

@Bean
@Primary
RedisConnectionFactory redisFactory() {
  return LettuceConnectionFactory.builder()
    .host(redis.getHost())
    .port(redis.getMappedPort(6379))
    .build();
}
```

### Kafka
```java
@Container
static KafkaContainer kafka = new KafkaContainer(
  DockerImageName.parse("confluentinc/cp-kafka:7.5.0")
);

// Producer test
KafkaProducer<String, String> producer = new KafkaProducer<>(
  Map.of(
    ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafka.getBootstrapServers(),
    ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName(),
    ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName()
  )
);
```

### Localstack (AWS)
```java
@Container
static LocalStackContainer localstack = new LocalStackContainer(
  DockerImageName.parse("localstack/localstack:2.3")
).withServices(S3, SQS, DYNAMODB);

S3Client s3 = S3Client.builder()
  .endpointOverride(localstack.getEndpointOverride(S3))
  .credentialsProvider(StaticCredentialsProvider.create(
    AwsBasicCredentials.create("test", "test")
  ))
  .region(Region.US_EAST_1)
  .build();
```

## 4. Python Testcontainers

```python
# pytest + testcontainers
from testcontainers.postgres import PostgresContainer
import psycopg2

def test_postgres():
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(postgres.get_connection_url())
        cur = conn.cursor()
        cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT)")
        cur.execute("INSERT INTO users (name) VALUES ('Alice')")
        conn.commit()
        cur.execute("SELECT * FROM users")
        assert cur.fetchone() == (1, "Alice")
```

## 5. Lifecycle Optimization

| Strategy | Use Case | Speed |
|----------|----------|-------|
| Per test class | Default, good isolation | Medium |
| Singleton container | Shared across suite | Fast |
| @RestartPerTest | Maximum isolation | Slow |

```java
// Singleton (faster)
@Testcontainers
public class SharedDbTest {
  @Container
  static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:15");
  // static = one container for all tests in class
}
```

## 6. Docker Compose

```java
@Container
static DockerComposeContainer<?> compose =
  new DockerComposeContainer<>(new File("docker-compose.test.yml"))
    .withExposedService("app", 8080)
    .withExposedService("db", 5432);

String appHost = compose.getServiceHost("app", 8080);
int appPort = compose.getServicePort("app", 8080);
```

## 7. CI/CD Requirements

- Docker daemon available (GitHub Actions `ubuntu-latest` has it)
- Ryuk container cleanup enabled by default
- Mount `/var/run/docker.sock` if running in Docker-in-Docker

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin' }
      - run: mvn test -Dtest='*Testcontainers*'
```

## 8. Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Using H2 in production, PG in tests | Use same DB in tests |
| `@Container` on non-static field | Container restarts per test method |
| Hardcoding ports | Use `getMappedPort()` |
| No schema init | Use `.withInitScript()` or Flyway |
| Ignoring container logs | Enable log streaming for debugging |

## 9. Related Resources

- Skills: `sql-server`, `postgresql` (if added), `flask-api`
- Prompts: `generate-integration-test-suite` (QA)
- Agents: `test-architect`
