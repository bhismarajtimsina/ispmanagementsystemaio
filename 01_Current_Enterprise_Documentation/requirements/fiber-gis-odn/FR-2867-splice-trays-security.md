# FR-2867 - Splice Trays - SECURITY

**Module:** Fiber GIS / ODN  
**Requirement type:** SECURITY  
**Primary actors:** Fiber Engineer, Network Engineer  

## Purpose
Defines permissions, isolation and audit controls for **Splice Trays**.

## Requirements
- Authorization is enforced in backend services and never trusted to hidden UI controls.
- Tenant ownership is checked before revealing object existence where data leakage is possible.
- Sensitive fields are masked and excluded from logs/exports unless explicitly permitted.
- Privileged actions write audit records with actor, reason, target and before/after context.
- Support-access or impersonation context is displayed and separately audited.
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
- FR-2867-A: Authorized actor can execute the allowed Splice Trays workflow and persistence survives restart.
- FR-2867-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-2867-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-2867-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
