# FR-0247 - Backup & Restore - BACKEND

**Module:** Superadmin Platform  
**Requirement type:** BACKEND  
**Primary actors:** CyberSathy Superadmin  

## Purpose
Defines authoritative backend behavior for **Backup & Restore** as part of platform control plane.

## Requirements
- Authoritative storage: platform database.
- Every request resolves authenticated tenant context before object lookup.
- Writes use transactions when multiple records must remain consistent.
- Background work returns a durable job ID, state, progress/error information and retry semantics.
- The service must reject unsupported state transitions with stable error codes.
- Domain rule: tenant support access is audited.
- Domain rule: entitlements are backend enforced.
- Domain rule: plan limits never rely on UI alone.

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
- FR-0247-A: Authorized actor can execute the allowed Backup & Restore workflow and persistence survives restart.
- FR-0247-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-0247-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-0247-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
