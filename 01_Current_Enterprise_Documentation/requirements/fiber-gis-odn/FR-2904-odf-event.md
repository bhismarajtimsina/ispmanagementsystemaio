# FR-2904 - ODF - EVENT

**Module:** Fiber GIS / ODN  
**Requirement type:** EVENT  
**Primary actors:** Fiber Engineer, Network Engineer  

## Purpose
Defines events and automation hooks emitted or consumed by **ODF**.

## Requirements
- Event names are stable, namespaced and include tenant ID, object IDs, event time and schema version.
- Consumers must be idempotent and tolerate duplicate delivery.
- Raw vendor events remain available for diagnosis while normalized events drive platform workflows.
- Events that represent observations carry collection timestamps and freshness.
- Domain rule: geometry never creates connectivity.
- Domain rule: fiber identity is segment/core/end UUID based.
- Domain rule: splices cannot fan out.

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
- FR-2904-A: Authorized actor can execute the allowed ODF workflow and persistence survives restart.
- FR-2904-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-2904-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-2904-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
