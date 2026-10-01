# FR-2606 - Route Monitoring - BACKEND

**Module:** NMS  
**Requirement type:** BACKEND  
**Primary actors:** NOC Operator, Network Engineer  

## Purpose
Defines authoritative backend behavior for **Route Monitoring** as part of network monitoring and observed operational state.

## Requirements
- Authoritative storage: device inventory plus time-series metrics.
- Every request resolves authenticated tenant context before object lookup.
- Writes use transactions when multiple records must remain consistent.
- Background work returns a durable job ID, state, progress/error information and retry semantics.
- The service must reject unsupported state transitions with stable error codes.
- Domain rule: stale telemetry is not equal to down.
- Domain rule: metric retention is time-series oriented.
- Domain rule: polling is capability-aware.

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
- FR-2606-A: Authorized actor can execute the allowed Route Monitoring workflow and persistence survives restart.
- FR-2606-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-2606-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-2606-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
