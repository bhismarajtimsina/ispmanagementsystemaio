# CLAUDE.md - FiberNet Enterprise

Read `books/00-master-index.md` and `MASTER-MANIFEST.csv` before changing domain models.

## Non-negotiable architecture
1. Do not make geographic map edges authoritative connectivity.
2. Do not let topology diagrams own connectivity.
3. Passive topology is modeled with typed termination nodes and typed edges in PostgreSQL/PostGIS.
4. Billing, AAA, NMS, device configuration, ACS/USP and Fiber GIS remain separate bounded contexts.
5. Every tenant-owned domain object is protected by backend tenant isolation.
6. Device credentials are secret references, never ordinary asset fields or logs.
7. Vendor-specific behavior lives in versioned adapters/drivers with capability declarations.
8. Unsupported capability must return unavailable, never fake success.
9. Device write jobs require validation, authorization, audit, job state and verification when supported.
10. Planned, documented-as-built and observed state must remain distinct.
11. Offline field edits are drafts until server validation/commissioning succeeds.
12. Stale polling means stale/unknown, not automatically offline.

## Required implementation sequence
Tenancy/identity -> entitlements/permissions -> customers/billing foundation -> authoritative fiber topology -> AAA -> NMS collectors -> device driver framework -> OLT/ONU -> ACS/USP -> field/automation -> scale.

## UI rules
Use the mockups under `ui/mockups/` as visual references. Preserve consistent sidebar/header/card/table/detail-drawer behavior. All write screens must expose pending/success/failure/conflict states. Color cannot be the only status cue. Large fiber tables must be virtualized.

## Definition of done
A feature is not implemented because its screen renders. It requires persistence, backend permission checks, tenant isolation, audit where applicable, error states and automated tests.
