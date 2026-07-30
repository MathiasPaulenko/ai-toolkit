# RemoteValue Match Patterns

> Complete guide to RemoteValue pattern matching in bidiwave for type-safe JavaScript result handling.

## What is RemoteValue

When you evaluate JavaScript via `page.evaluate()`, bidiwave returns a `RemoteValue` — a typed wrapper around the BiDi-serialized value. Instead of raw dicts, you use Python's `match` statement to extract the inner value in a type-safe way.

## RemoteValue Types

| Type | Python Class | Inner Value | Example JS |
|------|-------------|-------------|------------|
| String | `StringValue` | `str` | `"hello"` |
| Number | `NumberValue` | `int \| float` | `42`, `3.14` |
| Boolean | `BooleanValue` | `bool` | `true` |
| Null | `NullValue` | `None` | `null` |
| Undefined | `UndefinedValue` | `None` | `undefined` |
| Array | `ArrayValue` | `list[RemoteValue]` | `[1, 2, 3]` |
| Object | `ObjectValue` | `dict[str, RemoteValue]` | `{a: 1, b: 2}` |
| Symbol | `SymbolValue` | `str` | `Symbol("foo")` |
| BigInt | `BigIntValue` | `str` | `9007199254740993n` |
| Function | `FunctionValue` | `str` | `function() {}` |
| RegExp | `RegExpValue` | `RegExpInfo` | `/pattern/g` |
| Date | `DateValue` | `str` | `new Date()` |
| Map | `MapValue` | `list[tuple]` | `new Map()` |
| Set | `SetValue` | `list[RemoteValue]` | `new Set()` |
| WeakMap | `WeakMapValue` | `str` | `new WeakMap()` |
| WeakSet | `WeakSetValue` | `str` | `new WeakSet()` |
| Error | `ErrorValue` | `ErrorInfo` | `new Error("msg")` |
| Proxy | `ProxyValue` | `str` | `new Proxy({}, {})` |
| Promise | `PromiseValue` | `str` | `Promise.resolve()` |
| TypedArray | `TypedArrayValue` | `list` | `new Uint8Array()` |
| ArrayBuffer | `ArrayBufferValue` | `bytes` | `new ArrayBuffer(8)` |
| NodeList | `NodeListValue` | `list[NodeValue]` | `document.querySelectorAll("a")` |
| HTMLCollection | `HTMLCollectionValue` | `list[NodeValue]` | `document.children` |
| Node | `NodeValue` | `NodeInfo` | `document.body` |
| Window | `WindowValue` | `str` | `window` |

## Pattern Matching Examples

### Basic types

```python
from bidiwave import StringValue, NumberValue, BooleanValue, NullValue, UndefinedValue

result = await page.evaluate("document.title")
match result:
    case StringValue(value=title):
        print(f"Title: {title}")
    case _:
        print(f"Unexpected type: {result}")
```

### Number

```python
result = await page.evaluate("document.querySelectorAll('a').length")
match result:
    case NumberValue(value=count):
        assert count == 5
```

### Boolean

```python
result = await page.evaluate("document.hidden")
match result:
    case BooleanValue(value=hidden):
        assert hidden is False
```

### Null and undefined

```python
result = await page.evaluate("document.nonExistent")
match result:
    case NullValue():
        print("Element is null")
    case UndefinedValue():
        print("Property is undefined")
```

### Array

```python
from bidiwave import ArrayValue, StringValue

result = await page.evaluate("Array.from(document.querySelectorAll('a')).map(a => a.href)")
match result:
    case ArrayValue(value=items):
        for item in items:
            match item:
                case StringValue(value=href):
                    print(href)
```

### Object

```python
from bidiwave import ObjectValue, StringValue, NumberValue

result = await page.evaluate("({title: document.title, links: document.querySelectorAll('a').length})")
match result:
    case ObjectValue(value=props):
        match props.get("title"):
            case StringValue(value=title):
                print(f"Title: {title}")
        match props.get("links"):
            case NumberValue(value=count):
                print(f"Links: {count}")
```

### Nested structures

```python
result = await page.evaluate("""
({
    user: { name: "Alice", age: 30 },
    tags: ["admin", "active"],
})
""")
match result:
    case ObjectValue(value=props):
        match props.get("user"):
            case ObjectValue(value=user_props):
                match user_props.get("name"):
                    case StringValue(value=name):
                        assert name == "Alice"
        match props.get("tags"):
            case ArrayValue(value=tags):
                assert len(tags) == 2
```

### Date

```python
from bidiwave import DateValue

result = await page.evaluate("new Date().toISOString()")
match result:
    case DateValue(value=date_str):
        print(f"Date: {date_str}")
```

### Error

```python
from bidiwave import ErrorValue

try:
    result = await page.evaluate("undefinedVar.foo")
except Exception:
    pass

# Errors can also be returned as values
result = await page.evaluate("new Error('something went wrong')")
match result:
    case ErrorValue(message=msg, stack=stack):
        print(f"Error: {msg}")
        print(f"Stack: {stack}")
```

### RegExp

```python
from bidiwave import RegExpValue

result = await page.evaluate("/pattern/g")
match result:
    case RegExpValue(pattern=pat, flags=flags):
        print(f"Pattern: {pat}, flags: {flags}")
```

### Map

```python
from bidiwave import MapValue, StringValue, NumberValue

result = await page.evaluate("new Map([['a', 1], ['b', 2]])")
match result:
    case MapValue(value=entries):
        for key, val in entries:
            match key:
                case StringValue(value=k):
                    match val:
                        case NumberValue(value=v):
                            print(f"{k}: {v}")
```

### Set

```python
from bidiwave import SetValue, StringValue

result = await page.evaluate("new Set(['a', 'b', 'c'])")
match result:
    case SetValue(value=items):
        for item in items:
            match item:
                case StringValue(value=s):
                    print(s)
```

### NodeList

```python
from bidiwave import NodeListValue, NodeValue

result = await page.evaluate("document.querySelectorAll('div')")
match result:
    case NodeListValue(value=nodes):
        for node in nodes:
            match node:
                case NodeValue(node_type=t, local_name=name):
                    print(f"Node: {name}, type: {t}")
```

## Using `return_by_value=True`

When `return_by_value=True`, complex objects are serialized to JSON-compatible Python types:

```python
result = await page.evaluate(
    "({title: document.title, count: 42})",
    return_by_value=True,
)
# result is a plain dict: {"title": "Example Domain", "count": 42}
```

This bypasses `RemoteValue` and returns native Python types, but loses type safety.

## When to Use `match` vs `return_by_value`

| Approach | Pros | Cons |
|----------|------|------|
| `match` (default) | Type-safe, handles all JS types, preserves structure | More verbose, requires pattern matching |
| `return_by_value=True` | Simple, native Python types | Loses type info, fails on non-serializable values |

### Use `match` when

- Handling complex JS types (Map, Set, Date, RegExp, Error)
- Need type safety and exhaustive handling
- Working with DOM nodes or NodeLists

### Use `return_by_value=True` when

- Working with simple JSON-serializable data
- Quick prototyping
- Don't need type discrimination

## Exhaustive Matching

Always include a fallback case to handle unexpected types:

```python
result = await page.evaluate("someExpression")
match result:
    case StringValue(value=s):
        handle_string(s)
    case NumberValue(value=n):
        handle_number(n)
    case BooleanValue(value=b):
        handle_boolean(b)
    case NullValue():
        handle_null()
    case _:
        raise ValueError(f"Unexpected RemoteValue type: {type(result)}")
```

## Common Patterns

### Extract string or fallback

```python
result = await page.evaluate("document.querySelector('h1')?.textContent")
match result:
    case StringValue(value=heading):
        print(heading)
    case NullValue():
        print("No h1 found")
    case _:
        print("Unexpected result")
```

### Count elements

```python
result = await page.evaluate("document.querySelectorAll('.item').length")
match result:
    case NumberValue(value=count):
        assert count > 0, "Should have at least one item"
```

### Get attribute values

```python
result = await page.evaluate("""
    Array.from(document.querySelectorAll('a')).map(a => ({
        href: a.href,
        text: a.textContent.trim(),
    }))
""")
match result:
    case ArrayValue(value=items):
        links = []
        for item in items:
            match item:
                case ObjectValue(value=props):
                    match props.get("href"):
                        case StringValue(value=href):
                            match props.get("text"):
                                case StringValue(value=text):
                                    links.append({"href": href, "text": text})
```
