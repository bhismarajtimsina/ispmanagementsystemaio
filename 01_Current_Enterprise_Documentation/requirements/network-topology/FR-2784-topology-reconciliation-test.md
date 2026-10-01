# FR-2784 - Topology Reconciliation - TEST

**Module:** Network Topology  
**Requirement type:** TEST  
**Primary actors:** NOC Operator, Network Engineer  

## Purpose
Defines acceptance and regression testing for **Topology Reconciliation**.

## Requirements
- Test the happy path against real domain/service code, not a static mock.
- Test unauthorized role, wrong tenant, stale revision and malformed input paths.
- Test empty/unknown/stale operational data without converting it to a healthy state.
- Test idempotent retry behavior for relevant writes/jobs.
- Verify audit/event output for privileged changes.
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
- FR-2784-A: Authorized actor can execute the allowed Topology Reconciliation workflow and persistence survives restart.
- FR-2784-B: Cross-tenant identifier access is denied without leaking protected data.
- FR-2784-C: Unsupported or incomplete input produces an explicit non-success result.
- FR-2784-D: Audit/event output is generated for privileged state changes.

## Implementation notes
This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`.
