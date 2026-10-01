# FR-5233 - Vendor Device Adapter - SECURITY

**Module:** APIs & Integrations  
**Requirement type:** SECURITY  
**Primary actors:** API Client, Platform Support Engineer  

## Purpose
Defines permissions, isolation and audit controls for **Vendor Device Adapter**.

## Requirements
- Authorization is enforced in backend services and never trusted to hidden UI controls.
- Tenant ownership is checked before revealing object existence where data leakage is possible.
- Sensitive fields are masked and excluded from logs/exports unless explicitly permitted.
- Privileged actions write audit records with actor, reason, target and before/after context.
- Support-access or impersonation context is displayed and separately audited.
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
- FR-5233-A: Authorized actor can execute the allowed Vendor Device Adapter workflow and persistence survives restart.
- FR-5233-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-5233-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-5233-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
