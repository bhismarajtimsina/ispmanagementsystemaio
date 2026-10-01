# FR-0717 - TR-069 Data Models - API

**Module:** ONT / ONU Platform  
**Requirement type:** API  
**Primary actors:** Network Engineer, NOC Operator  

## Purpose
Defines the versioned API contract required to expose **TR-069 Data Models** safely.

## Requirements
- Use `/api/v1` style versioning and stable UUID identifiers.
- List endpoints support pagination, filters and explicit sort keys.
- Retryable writes accept idempotency keys where duplicate side effects are possible.
- 409 Conflict is used for stale revisions or resource occupancy conflicts.
- Responses include machine-readable error codes, human explanation and affected IDs when safe.
- Domain rule: documented source and observed source are separate.
- Domain rule: registration authentication methods are model aware.
- Domain rule: replacement preserves history.

## Required UI / service states
- `loading`
- `empty`
- `healthy`
- `warning`
- `critical`
- `unknown`
- `stale`
- `offline`
- `permission-denied`
- `conflict`
- `validation-error`
- `partial-data`

## Core fields

| Field | Rule |
|---|---|
| Tenant / organization | Resolved from authenticated context; not accepted blindly from the client. |
| Stable identifier | UUID or documented external ID; display names are not foreign keys. |
| Status | Normalized state with explicit unknown/stale handling. |
| Created/updated metadata | UTC timestamps plus actor/source where applicable. |
| Notes / reason | Required for selected privileged or exception operations. |

## Permissions
- `view` for read access.
- `create` and `edit` are separate permissions.
- `approve`/`execute` are distinct for controlled changes.
- `export` is separately auditable.

## API expectations
- Stable identifiers and versioned endpoints.
- Pagination/filtering for collections.
- Consistent error envelope.
- Request correlation ID for privileged jobs.

## Audit and events
- Audit privileged writes.
- Emit normalized domain events after durable state change.
- Never log plaintext device/customer secrets.

## Acceptance checks
- FR-0717-A: Authorized actor can execute the allowed TR-069 Data Models workflow and persistence survives restart.
- FR-0717-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-0717-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-0717-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
