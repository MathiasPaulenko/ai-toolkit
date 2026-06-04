---
name: Java Coding Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Coding standards and conventions for Java projects. Covers Google Java Style, Spring Boot conventions, Lombok usage, exception handling, and modern Java idioms.
tags: [java, coding-rules, style-guide, spring-boot, lombok, google-java-style]
role: coding-standard
type: rules
language: en
---

# Java Coding Rules

## 1. Code Style

Follow **Google Java Style** with these specifics:

- **2-space indent** (not 4).
- **100-column line limit**.
- No wildcard imports (`import java.util.*`).
- One statement per line.
- Braces required for all control structures.

```java
// Good
if (user.isActive()) {
  return user.getName();
}

// Bad
if (user.isActive()) return user.getName();
```

## 2. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | `PascalCase` | `UserService`, `OrderRepository` |
| Interfaces | `PascalCase` (adjective-like) | `Authenticatable`, `Serializable` |
| Methods | `camelCase` (verb first) | `getUserById`, `processOrder` |
| Variables | `camelCase` | `userList`, `orderCount` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_ATTEMPTS` |
| Packages | `lowercase` | `com.example.userservice` |
| Enums | `PascalCase`, constants `UPPER_SNAKE_CASE` | `Status.ACTIVE` |

## 3. Lombok Usage

Use Lombok to reduce boilerplate, but avoid overuse:

```java
// Good
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDto {
  private String id;
  private String email;
  private UserRole role;
}

// Good — immutable value object
@Value
public class Money {
  BigDecimal amount;
  Currency currency;
}

// Bad — @Data on entity (equals/hashCode can be problematic with JPA)
@Entity
@Data  // Avoid: can cause LazyInitializationException with @EqualsAndHashCode
public class User { ... }

// Good — entity
@Entity
@Getter
@Setter
@NoArgsConstructor
public class User { ... }
```

## 4. Spring Boot Conventions

### Constructor Injection (mandatory)

```java
// Good
@Service
public class UserService {
  private final UserRepository userRepository;
  private final EmailService emailService;

  public UserService(UserRepository userRepository, EmailService emailService) {
    this.userRepository = userRepository;
    this.emailService = emailService;
  }
}

// Bad — field injection
@Service
public class UserService {
  @Autowired
  private UserRepository userRepository;  // Do not use
}
```

### Service Layer

```java
@Service
@Transactional(readOnly = true)
public class OrderService {

  @Transactional
  public Order createOrder(CreateOrderCommand command) {
    // business logic
  }

  public Optional<Order> findById(String id) {
    return orderRepository.findById(id);
  }
}
```

### Controller

```java
@RestController
@RequestMapping("/api/v1/orders")
@Validated
@RequiredArgsConstructor
public class OrderController {
  private final OrderService orderService;

  @GetMapping("/{id}")
  public ResponseEntity<OrderDto> getOrder(@PathVariable String id) {
    return orderService.findById(id)
        .map(ResponseEntity::ok)
        .orElse(ResponseEntity.notFound().build());
  }

  @PostMapping
  public ResponseEntity<OrderDto> createOrder(
      @RequestBody @Valid CreateOrderRequest request) {
    // ...
  }
}
```

## 5. Exception Handling

- Use custom exceptions for domain errors.
- Use `@ControllerAdvice` for global exception handling.
- Never swallow exceptions.
- Include correlation IDs in error responses.

```java
@ControllerAdvice
public class GlobalExceptionHandler {

  @ExceptionHandler(NotFoundException.class)
  public ResponseEntity<ErrorResponse> handleNotFound(NotFoundException ex) {
    return ResponseEntity
        .status(HttpStatus.NOT_FOUND)
        .body(new ErrorResponse(ex.getMessage(), ex.getResource()));
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<ValidationErrorResponse> handleValidation(
      MethodArgumentNotValidException ex) {
    List<String> errors = ex.getBindingResult().getFieldErrors().stream()
        .map(e -> e.getField() + ": " + e.getDefaultMessage())
        .toList();
    return ResponseEntity.badRequest()
        .body(new ValidationErrorResponse(errors));
  }
}
```

## 6. Modern Java Idioms

- Use `var` for local variables when type is obvious.
- Use `Optional<T>` to avoid null checks.
- Use `Stream API` for collection transformations.
- Use `List.of()`, `Map.of()`, `Set.of()` for immutable collections.
- Use `records` (Java 16+) for DTOs and command objects.

```java
// Good
var users = userRepository.findAll();
var activeUsers = users.stream()
    .filter(User::isActive)
    .map(User::getEmail)
    .toList();

// Good
Optional<User> user = userRepository.findById(id);
user.ifPresentOrElse(
    u -> emailService.sendWelcome(u),
    () -> log.warn("User not found: {}", id)
);

// Good — record for DTO
public record UserDto(String id, String email, UserRole role) {}

// Good — pattern matching (Java 17+)
if (obj instanceof User user) {
  System.out.println(user.getEmail());
}
```

## 7. Testing

- Use **JUnit 5** (`@Test`, `@ParameterizedTest`, `@Nested`).
- Use **Mockito** for mocking.
- Use **AssertJ** for fluent assertions.
- Use **TestContainers** for integration tests.

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

  @Mock
  private UserRepository userRepository;

  @InjectMocks
  private UserService userService;

  @Test
  void shouldReturnUser_whenUserExists() {
    var user = new User("1", "alice@example.com");
    when(userRepository.findById("1")).thenReturn(Optional.of(user));

    var result = userService.findById("1");

    assertThat(result)
        .isPresent()
        .hasValueSatisfying(u -> assertThat(u.getEmail()).isEqualTo("alice@example.com"));
  }
}
```

## 8. Documentation

- Use **Javadoc** on all public APIs.
- Document `@param`, `@return`, `@throws`.
- Include code examples for complex operations.

```java
/**
 * Authenticates a user by credentials and returns a JWT token.
 *
 * @param username the user's login name (case-insensitive)
 * @param password the user's plain-text password
 * @return a JWT token valid for 24 hours
 * @throws AuthenticationException if credentials are invalid
 * @throws AccountLockedException if the account is temporarily locked
 */
public String authenticate(String username, String password) { ... }
```

## 9. Build and Tooling

- Use **Maven** or **Gradle** with Kotlin DSL.
- Pin dependency versions; do not use `LATEST` or `RELEASE`.
- Use **Spotless** for code formatting.
- Use **SonarQube** for quality gates.
- Use **Checkstyle** with Google Style config.

```xml
<!-- pom.xml plugins -->
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>2.43.0</version>
  <configuration>
    <java>
      <googleJavaFormat/>
    </java>
  </configuration>
</plugin>
```
