# FR-4243 - Maintenance Windows - UI

**Module:** Configuration & Automation  
**Requirement type:** UI  
**Primary actors:** Network Engineer  

## Purpose
Defines the frontend experience for **Maintenance Windows** within the Configuration & Automation module.

## Requirements
- Primary menu path: `Configuration & Automation > Maintenance Windows`.
- Primary actors: Network Engineer.
- The screen must support responsive desktop layout and an accessible keyboard path for all critical actions.
- Tables must support server-side pagination/filtering where data volume can be large.
- Context drawers must preserve the user's list/map position when opened and closed.
- Destructive or high-risk actions require a confirmation surface that states scope and expected impact.
- Domain rule: writes require capability support.
- Domain rule: dry-run/preview precedes high-risk action.
- Domain rule: read-back verification is preferred.

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
- FR-4243-A: Authorized actor can execute the allowed Maintenance Windows workflow and persistence survives restart.
- FR-4243-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-4243-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-4243-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
