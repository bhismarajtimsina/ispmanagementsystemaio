# FR-0687 - Ethernet Ports - UI

**Module:** ONT / ONU Platform  
**Requirement type:** UI  
**Primary actors:** Network Engineer, NOC Operator  

## Purpose
Defines the frontend experience for **Ethernet Ports** within the ONT / ONU Platform module.

## Requirements
- Primary menu path: `ONT / ONU Platform > Ethernet Ports`.
- Primary actors: Network Engineer, NOC Operator.
- The screen must support responsive desktop layout and an accessible keyboard path for all critical actions.
- Tables must support server-side pagination/filtering where data volume can be large.
- Context drawers must preserve the user's list/map position when opened and closed.
- Destructive or high-risk actions require a confirmation surface that states scope and expected impact.
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
- FR-0687-A: Authorized actor can execute the allowed Ethernet Ports workflow and persistence survives restart.
- FR-0687-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-0687-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-0687-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
