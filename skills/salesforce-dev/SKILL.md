---
name: salesforce-dev
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Salesforce development guide. Covers Apex triggers, Lightning Web Components (LWC), SOQL, SOSL, platform events, and deployment via SFDX.
tags: [salesforce, apex, lwc, soql, sfdx, crm]
role: salesforce-developer
model: any
trigger: When the user mentions Salesforce, Apex, LWC, SOQL, SOSL, platform events, SFDX, or Salesforce DX.
---

# Salesforce Development

## 1. Apex

### Trigger

```apex
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            AccountTriggerHandler.beforeInsert(Trigger.new);
        } else if (Trigger.isUpdate) {
            AccountTriggerHandler.beforeUpdate(Trigger.new, Trigger.oldMap);
        }
    } else if (Trigger.isAfter) {
        if (Trigger.isInsert) {
            AccountTriggerHandler.afterInsert(Trigger.new);
        }
    }
}
```

### Handler Class

```apex
public with sharing class AccountTriggerHandler {
    public static void beforeInsert(List<Account> newAccounts) {
        for (Account acc : newAccounts) {
            if (String.isBlank(acc.Industry)) {
                acc.Industry.addError('Industry is required');
            }
        }
    }

    public static void afterInsert(List<Account> newAccounts) {
        List<Task> tasks = new List<Task>();
        for (Account acc : newAccounts) {
            tasks.add(new Task(
                Subject = 'Follow up with new account',
                WhatId = acc.Id,
                Status = 'Not Started',
                Priority = 'Normal'
            ));
        }
        insert tasks;
    }
}
```

### SOQL

```apex
// Basic query
List<Account> accounts = [
    SELECT Id, Name, Industry, (SELECT Name FROM Contacts)
    FROM Account
    WHERE Industry = 'Technology'
    WITH SECURITY_ENFORCED
    LIMIT 100
];

// Aggregate
AggregateResult[] results = [
    SELECT Industry, COUNT(Id) cnt
    FROM Account
    GROUP BY Industry
    HAVING COUNT(Id) > 5
];

// Dynamic SOQL
String query = 'SELECT Id, Name FROM Account WHERE Industry = :industry';
List<Account> accs = Database.query(query);
```

## 2. Lightning Web Components (LWC)

### Component Structure

```
myComponent/
  myComponent.html
  myComponent.js
  myComponent.js-meta.xml
  myComponent.css
```

### JavaScript

```javascript
// myComponent.js
import { LightningElement, wire, api, track } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import getAccounts from '@salesforce/apex/AccountController.getAccounts';

const FIELDS = ['Account.Name', 'Account.Industry'];

export default class MyComponent extends LightningElement {
    @api recordId;
    @track accounts = [];
    error;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    wiredRecord({ error, data }) {
        if (data) {
            this.account = data;
        } else if (error) {
            this.error = error;
        }
    }

    @wire(getAccounts)
    wiredAccounts({ error, data }) {
        if (data) {
            this.accounts = data;
        } else if (error) {
            this.error = error;
        }
    }

    handleSelect(event) {
        const selectedId = event.target.dataset.id;
        // Handle selection
    }
}
```

### HTML Template

```html
<!-- myComponent.html -->
<template>
    <lightning-card title="Account List" icon-name="standard:account">
        <template if:true={accounts}>
            <lightning-datatable
                key-field="id"
                data={accounts}
                columns={columns}
                onrowselection={handleSelect}>
            </lightning-datatable>
        </template>
        <template if:true={error}>
            <div class="slds-text-color_error">{error.body.message}</div>
        </template>
    </lightning-card>
</template>
```

### Meta XML

```xml
<!-- myComponent.js-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
    </targets>
</LightningComponentBundle>
```

## 3. SFDX (Salesforce DX)

### Project Setup

```bash
sfdx force:project:create -n my-project
cd my-project
sfdx auth:web:login -a devhub
sfdx force:org:create -f config/project-scratch-def.json -a scratch -s -d 7
```

### Deploy

```bash
# Deploy source
sfdx force:source:deploy -p force-app/main/default

# Retrieve changes
sfdx force:source:retrieve -p force-app/main/default

# Run tests
sfdx force:apex:test:run -n AccountTriggerTest -r human
```

### Package Development

```bash
# Create unlocked package
sfdx force:package:create -n "My Package" -r force-app -t Unlocked -v devhub

# Create package version
sfdx force:package:version:create -p "My Package" -x -c

# Install in org
sfdx force:package:install -p "My Package@1.0.0-1" -u target-org
```

## 4. Platform Events

```apex
// Publish event
EventBus.publish(new Customer_Event__e(
    Account_Id__c = acc.Id,
    Event_Type__c = 'CREATED'
));

// Subscribe via trigger
trigger CustomerEventTrigger on Customer_Event__e (after insert) {
    for (Customer_Event__e event : Trigger.new) {
        // Process event
    }
}
```

## 5. Testing

```apex
@isTest
private class AccountTriggerTest {
    @isTest
    static void testBeforeInsert() {
        Account acc = new Account(Name = 'Test', Industry = '');

        Test.startTest();
        Database.SaveResult result = Database.insert(acc, false);
        Test.stopTest();

        System.assert(!result.isSuccess(), 'Should fail without Industry');
    }

    @isTest
    static void testAfterInsert() {
        Account acc = new Account(Name = 'Test', Industry = 'Technology');

        Test.startTest();
        insert acc;
        Test.stopTest();

        List<Task> tasks = [SELECT Id FROM Task WHERE WhatId = :acc.Id];
        System.assertEquals(1, tasks.size(), 'Task should be created');
    }
}
```

## 6. Security

- Use `with sharing` / `without sharing` / `inherited sharing` explicitly.
- Use `WITH SECURITY_ENFORCED` in SOQL.
- Validate CRUD/FLS before DML operations.
- Use `stripInaccessible` for safe object mapping.

```apex
SObjectAccessDecision decision = Security.stripInaccessible(
    AccessType.CREATABLE,
    new List<Account>{ acc }
);
insert decision.getRecords();
```
