---
name: appian-lowcode
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Appian low-code platform development guide. Covers process models, SAIL interfaces, data stores, expressions, integrations, and deployment best practices.
tags: [appian, low-code, bpm, process-model, sail, enterprise]
role: appian-developer
model: any
trigger: When the user mentions Appian, low-code, BPM, process models, SAIL, data stores, or Appian expressions.
---

# Appian Low-Code

## 1. Process Models

### Basic Process

```
Start Event â†’ User Input Task â†’ Exclusive Gateway â†’ [Approved] â†’ Write to Database â†’ End Event
                                    |
                                    +-- [Rejected] â†’ Send Notification â†’ End Event
```

### Node Types

| Node | Purpose |
|------|---------|
| Start Event | Process initiation |
| User Input Task | Form for user data entry |
| Automated Activity | Executes expression or smart service |
| Exclusive Gateway | Conditional branching (XOR) |
| Parallel Gateway | Parallel execution (AND) |
| Subprocess | Reusable process segment |
| End Event | Process termination |

### Best Practices

- Keep processes under 50 nodes for readability.
- Use subprocesses for reusable logic.
- Name lanes by role (e.g., "Manager", "HR Specialist").
- Set due dates on all user tasks.
- Use process reports for monitoring SLA compliance.

## 2. SAIL Interfaces

### Form Layout

```sail
a!localVariables(
  local!formData: {
    name: "",
    email: "",
    priority: ""
  },
  
  a!formLayout(
    label: "Request Form",
    contents: {
      a!textField(
        label: "Name",
        value: local!formData.name,
        saveInto: local!formData.name,
        required: true
      ),
      a!textField(
        label: "Email",
        value: local!formData.email,
        saveInto: local!formData.email,
        validations: a!emailValidation()
      ),
      a!dropdownField(
        label: "Priority",
        value: local!formData.priority,
        saveInto: local!formData.priority,
        choiceLabels: {"Low", "Medium", "High"},
        choiceValues: {"LOW", "MED", "HIGH"}
      )
    },
    buttons: a!buttonLayout(
      primaryButtons: {
        a!buttonWidget(
          label: "Submit",
          value: local!formData,
          saveInto: ri!processVariable,
          submit: true
        )
      }
    )
  )
)
```

### Grid Layout

```sail
a!gridField(
  label: "Orders",
  data: local!orders,
  columns: {
    a!gridTextColumn(
      label: "Order ID",
      field: "id",
      alignment: "RIGHT"
    ),
    a!gridTextColumn(
      label: "Customer",
      field: "customerName"
    ),
    a!gridTextColumn(
      label: "Total",
      field: "total",
      alignment: "RIGHT"
    )
  },
  validations: if(
    a!isNullOrEmpty(local!orders),
    a!validationMessage("At least one order is required"),
    null
  )
)
```

## 3. Data Stores

### Entity Design

```
Employee
â”œâ”€â”€ id (Number, Primary Key)
â”œâ”€â”€ firstName (Text, Required)
â”œâ”€â”€ lastName (Text, Required)
â”œâ”€â”€ email (Text, Required, Unique)
â”œâ”€â”€ department (Text, Dropdown)
â”œâ”€â”€ hireDate (Date)
â”œâ”€â”€ isActive (Boolean, Default: true)
â””â”€â”€ managerId (Number, Foreign Key â†’ Employee.id)
```

### Querying

```sail
// Query all active employees
a!queryEntity(
  entity: cons!EMPLOYEE_ENTITY,
  query: a!query(
    selection: a!querySelection(columns: {
      a!queryColumn(field: "firstName"),
      a!queryColumn(field: "lastName"),
      a!queryColumn(field: "department")
    }),
    filter: a!queryFilter(
      field: "isActive",
      operator: "=",
      value: true
    ),
    pagingInfo: a!pagingInfo(startIndex: 1, batchSize: 50)
  )
)

// Aggregate: count by department
a!queryEntity(
  entity: cons!EMPLOYEE_ENTITY,
  query: a!query(
    aggregation: a!queryAggregation(
      aggregationColumns: {
        a!queryAggregationColumn(field: "department", isGrouping: true),
        a!queryAggregationColumn(field: "id", aggregationFunction: "COUNT")
      }
    )
  )
)
```

## 4. Expressions

### Common Functions

| Function | Purpose |
|----------|---------|
| `a!if()` | Conditional logic |
| `a!forEach()` | Iterate over lists |
| `a!index()` | Find index in list |
| `a!isNullOrEmpty()` | Null/empty check |
| `a!toDate()` | Parse string to date |
| `a!dateDiff()` | Calculate date difference |
| `a!userDisplayName()` | Get user display name |
| `a!loggedInUser()` | Current user info |

```sail
// Calculate SLA deadline
a!localVariables(
  local!createdDate: ri!ticket.createdDate,
  local!priority: ri!ticket.priority,
  local!slaHours: if(local!priority = "HIGH", 4, if(local!priority = "MED", 24, 72)),
  local!deadline: a!addDateTime(local!createdDate, "hour", local!slaHours),
  
  if(
    local!deadline < now(),
    a!richTextDisplayField(
      labelPosition: "COLLAPSED",
      value: a!richTextItem(
        text: "OVERDUE",
        style: "STRONG",
        color: "NEGATIVE"
      )
    ),
    local!deadline
  )
)
```

## 5. Integrations

### Web API (REST)

```sail
// Integration object: int!GetWeather
// HTTP Method: GET
// URL: https://api.weather.com/v1/current?location={location}

a!localVariables(
  local!weather: int!GetWeather(location: "New York"),
  
  if(
    local!weather.success,
    local!weather.result.temperature,
    "Error: " & local!weather.error.message
  )
)
```

### Connected Systems

- **OpenAPI/Swagger**: Import API spec to generate integration automatically.
- **SOAP**: Use WSDL import for legacy services.
- **Database**: JDBC connections for external databases.
- **RPA**: UiPath or Blue Prism integration for legacy automation.

## 6. Deployment

### Application Packages

```
Application Package
â”œâ”€â”€ Process Models
â”œâ”€â”€ SAIL Interfaces
â”œâ”€â”€ Data Stores & Records
â”œâ”€â”€ Expression Rules
â”œâ”€â”€ Connected Systems
â”œâ”€â”€ Document Templates
â””â”€â”€ Security: Groups & Folders
```

### Deployment Steps

1. **Export** application package from development environment.
2. **Import** to target environment (test/staging/prod).
3. **Inspect** import status for conflicts.
4. **Configure** environment-specific constants (URLs, credentials).
5. **Run** post-deployment tests.
6. **Update** security mappings if needed.

### Constants for Environment URLs

```sail
// In each environment, set:
cons!API_BASE_URL: "https://api-dev.example.com"  // Dev
cons!API_BASE_URL: "https://api-prod.example.com" // Prod
```

## 7. Security

- Use **Appian groups** for role-based access.
- Set record-level security in data stores.
- Use **service accounts** for integrations (not personal credentials).
- Audit process history for compliance.
- Mask sensitive fields (PII, SSN) in interfaces.

## 8. Testing

- Use **process reports** to verify flow completion.
- Test expressions in the expression editor before deploying.
- Use **test cases** on expression rules.
- Verify integrations with mock data in dev.
- Perform UAT with business users on staging.
