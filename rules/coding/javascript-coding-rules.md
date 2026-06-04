---
name: JavaScript Coding Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Coding standards and conventions for JavaScript and TypeScript projects. Covers ESLint-configured rules, async/await patterns, module structure, and modern JS/TS idioms.
tags: [javascript, typescript, coding-rules, style-guide, eslint, async-await]
role: coding-standard
type: rules
language: en
---

# JavaScript Coding Rules

## 1. Language Preference

- Use **TypeScript** for all new projects.
- Use **ES2022+** features (optional chaining, nullish coalescing, top-level await where appropriate).
- Target **ES2020** for transpiled output (broad compatibility).

## 2. Variable Declarations

- Use `const` by default.
- Use `let` only when reassignment is necessary.
- Never use `var`.

```typescript
// Good
const user = await fetchUser(id);
let attempts = 0;
attempts++;

// Bad
var user = await fetchUser(id);
```

## 3. Async/Await

- Prefer `async/await` over `.then()/.catch()` chains.
- Use `Promise.all()` for independent parallel operations.
- Handle errors with `try/catch` or `.catch()` at call site.

```typescript
// Good
async function loadDashboard(): Promise<DashboardData> {
  const [user, orders, notifications] = await Promise.all([
    fetchUser(),
    fetchOrders(),
    fetchNotifications(),
  ]);
  return { user, orders, notifications };
}

// Bad
function loadDashboard() {
  return fetchUser().then(user =>
    fetchOrders().then(orders =>
      fetchNotifications().then(notifications =>
        ({ user, orders, notifications })
      )
    )
  );
}
```

## 4. TypeScript Types

- Use `interface` for object shapes that may be extended.
- Use `type` for unions, tuples, and complex mapped types.
- Use `unknown` instead of `any` for values of uncertain type.
- Use `never` for exhaustive checks.

```typescript
// Good
interface User {
  id: string;
  email: string;
  role: 'admin' | 'editor' | 'viewer';
}

type ApiResponse<T> = { data: T } | { error: ApiError };

function process(value: unknown): string {
  if (typeof value === 'string') return value;
  return JSON.stringify(value);
}
```

## 5. Equality and Comparison

- Always use **strict equality** (`===`, `!==`).
- Use nullish coalescing (`??`) for default values.
- Use optional chaining (`?.`) for nested property access.

```typescript
// Good
if (user.role === 'admin') { ... }
const name = user.name ?? 'Anonymous';
const street = user.address?.street;

// Bad
if (user.role == 'admin') { ... }
const name = user.name || 'Anonymous';  // Wrong for empty string
```

## 6. Functions

- Use **arrow functions** for callbacks and closures.
- Use **named functions** for top-level exports (better stack traces).
- Prefer single-responsibility functions.
- Use destructuring for parameters.

```typescript
// Good
export function formatUser({ name, email, createdAt }: User): string {
  return `${name} <${email}> (joined ${createdAt.toDateString()})`;
}

const activeUsers = users.filter(user => user.isActive);

// Bad
function formatUser(user) {
  return user.name + ' <' + user.email + '>';
}
```

## 7. Modules

- Use **ES modules** (`import`/`export`).
- Avoid default exports for libraries; use named exports.
- Group imports: external → internal → types.
- Use `import type` for type-only imports.

```typescript
// Good
import React from 'react';
import type { ReactNode } from 'react';

import { UserCard } from '@/components/UserCard';
import type { User } from '@/types';

// Bad
const React = require('react');
```

## 8. Error Handling

- Create custom `Error` subclasses for domain errors.
- Always handle Promise rejections.
- Use `Result<T, E>` pattern for synchronous operations that may fail.

```typescript
// Good
class ValidationError extends Error {
  constructor(public fields: Record<string, string>) {
    super('Validation failed');
  }
}

try {
  await submitForm(data);
} catch (error) {
  if (error instanceof ValidationError) {
    showFieldErrors(error.fields);
  } else {
    showGenericError();
    console.error(error);
  }
}
```

## 9. React / Component Rules

- Use **functional components** with hooks.
- Use `React.FC` sparingly; prefer explicit props interfaces.
- Extract logic into custom hooks.
- Memoize expensive computations with `useMemo`.
- Memoize callbacks with `useCallback` when passed to optimized children.
- Use `key` prop correctly in lists.

```typescript
// Good
interface UserListProps {
  users: User[];
  onSelect: (id: string) => void;
}

export function UserList({ users, onSelect }: UserListProps): JSX.Element {
  const sortedUsers = useMemo(() =>
    [...users].sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  );

  return (
    <ul>
      {sortedUsers.map(user => (
        <li key={user.id}>
          <button onClick={() => onSelect(user.id)}>{user.name}</button>
        </li>
      ))}
    </ul>
  );
}
```

## 10. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Files | `kebab-case.ts` | `user-service.ts` |
| Components | `PascalCase.tsx` | `UserProfile.tsx` |
| Functions | `camelCase` | `fetchUserById` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Interfaces | `PascalCase` | `UserRepository` |
| Types | `PascalCase` | `ApiResponse` |
| Enums | `PascalCase`, members `UPPER_SNAKE_CASE` | `Status.ACTIVE` |
| Boolean vars | `is`/`has`/`should` prefix | `isLoading`, `hasPermission` |

## 11. Linting and Formatting

Use **ESLint** + **Prettier** + **TypeScript**:

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "no-console": ["warn", { "allow": ["error"] }]
  }
}
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

## 12. Testing

- Use **Vitest** or **Jest** for unit tests.
- Use **React Testing Library** for component tests.
- Use **Playwright** for E2E tests.
- Use **MSW** (Mock Service Worker) for API mocking.

```typescript
// Good
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserCard } from './UserCard';

test('displays user name and triggers click', async () => {
  const handleSelect = vi.fn();
  render(<UserCard user={mockUser} onSelect={handleSelect} />);

  expect(screen.getByText(mockUser.name)).toBeInTheDocument();

  await userEvent.click(screen.getByRole('button'));
  expect(handleSelect).toHaveBeenCalledWith(mockUser.id);
});
```
