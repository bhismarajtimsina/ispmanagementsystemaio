# FR-2381 - Interfaces - UI

**Module:** NMS  
**Requirement type:** UI  
**Primary actors:** NOC Operator, Network Engineer  

## Purpose
Defines the frontend experience for **Interfaces** within the NMS module.

## Requirements
- Primary menu path: `NMS > Interfaces`.
- Primary actors: NOC Operator, Network Engineer.
- The screen must support responsive desktop layout and an accessible keyboard path for all critical actions.
- Tables must support server-side pagination/filtering where data volume can be large.
- Context drawers must preserve the user's list/map position when opened and closed.
- Destructive or high-risk actions require a confirmation surface that states scope and expected impact.
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
- FR-2381-A: Authorized actor can execute the allowed Interfaces workflow and persistence survives restart.
- FR-2381-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-2381-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-2381-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
