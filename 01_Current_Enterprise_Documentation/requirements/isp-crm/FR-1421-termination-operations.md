# FR-1421 - Termination - OPERATIONS

**Module:** ISP CRM  
**Requirement type:** OPERATIONS  
**Primary actors:** ISP Administrator, Customer Support Agent  

## Purpose
Defines operational and failure-handling requirements for **Termination**.

## Requirements
- Operator-visible state must distinguish pending, partial, failed and complete work.
- Retry policies use bounded attempts/backoff and preserve the last vendor/system error safely.
- Runbooks identify rollback or safe-stop behavior for partially completed actions.
- Metrics expose latency, error count and saturation where relevant.
- Domain rule: backend authorization is mandatory.
- Domain rule: state transitions are explicit.
- Domain rule: audit applies to privileged writes.

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
- FR-1421-A: Authorized actor can execute the allowed Termination workflow and persistence survives restart.
- FR-1421-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-1421-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-1421-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
