# FR-1765 - Reseller HotSpot - UI

**Module:** Reseller Management  
**Requirement type:** UI  
**Primary actors:** ISP Administrator, Reseller Owner  

## Purpose
Defines the frontend experience for **Reseller HotSpot** within the Reseller Management module.

## Requirements
- Primary menu path: `Reseller Management > Reseller HotSpot`.
- Primary actors: ISP Administrator, Reseller Owner.
- The screen must support responsive desktop layout and an accessible keyboard path for all critical actions.
- Tables must support server-side pagination/filtering where data volume can be large.
- Context drawers must preserve the user's list/map position when opened and closed.
- Destructive or high-risk actions require a confirmation surface that states scope and expected impact.
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
- FR-1765-A: Authorized actor can execute the allowed Reseller HotSpot workflow and persistence survives restart.
- FR-1765-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-1765-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-1765-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
