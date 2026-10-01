# CLAUDE.md - CyberSathy FiberNet Implementation Rules

This repository implements CyberSathy FiberNet, an ISP fiber mapping and optical distribution network management application. Read this file and the linked documentation before changing the domain model.

## Required reading order

1. `docs/01-product-and-scope.md`
2. `docs/06-data-model-and-topology.md`
3. `docs/03-ui-ux-screenbook.md`
4. `docs/08-optical-engineering.md`
5. `docs/09-change-management.md`
6. `docs/13-testing-and-quality.md`
7. The phase-specific implementation section in `docs/16-implementation-roadmap.md`

## Primary invariant

Accurate core-and-port connectivity is the source of truth. The map, topology graph, closure drawing, cable core table, cached trace, and ONU tree are views over persisted domain data. Never make a visual edge authoritative by itself.

## Physical-model rules

- A `Fiber` belongs to a `CableSegment` and owns exactly two termination nodes through its two fiber ends.
- A fusion splice is one external `Connection` between exactly two eligible termination nodes.
- A normal splice cannot fan out.
- A splitter/coupler owns an input port, explicit physical output ports, and internal `OpticalTransfer` paths.
- Unequal branch ratios are attached to physical output identifiers, never left/right screen position.
- An uncut mid-span strand uses continuity semantics and must not add splice loss.
- Patch cords, adapters, ODF ports, pigtails, and attenuators are explicit components/ports where required for correct path accounting.
- Crossing geographic polylines never create a connection.
- A closure is an enclosure; it does not split power by itself.
- The persistent root is an OLT PON port. Replaceable optical modules have their own inventory/history.

## Topology rules

- Physical fiber spans and ordinary splices are bidirectionally traversable.
- Splitter/coupler transfer is input-to-output downstream and reversed only for upstream trace. Never traverse output-to-sibling-output.
- A commissioned active service path must resolve to one upstream PON root.
- Reject conflicting roots and closed active passive optical loops.
- Never manufacture a source for a dangling fiber.
- A damaged connected fiber may remain documented in as-built topology; the path becomes failed/blocked rather than being deleted.

## Optical rules

- Optical calculations belong in deterministic backend domain services.
- Every path result must include wavelength/direction, source power, receiver limits, fiber loss, connection loss, component transfer losses, engineering margin, and parameter provenance.
- For branch fraction `r`, ideal loss is `-10*log10(r)`.
- If manufacturer total insertion loss is supplied for a transfer path, use it directly; do not add ideal split loss again.
- Calculate upstream and downstream independently.
- Check sensitivity and overload separately.
- Engineering margin is reserve, not a physical loss to subtract twice.
- Missing optical parameters produce unknown/incomplete status, not a pass.
- Count each physical loss element once using stable loss-element identity.

## Revision and concurrency rules

- User edits occur in `ChangeSet` drafts against a `base_revision`.
- Commissioning runs final validation inside the same database transaction as the topology commit.
- Lock or serialize affected termination endpoints and use optimistic revision checks.
- Return HTTP 409 for stale base revision or endpoint occupancy conflicts.
- Never partially commission a set of topology edits.
- As-built topology revisions are immutable.
- Rollback means a new verified change/revision, not pretending field work was undone.

## Planned / as-built / observed

Keep these layers separate:

- Planned: proposed route/equipment/connectivity.
- As-built: commissioned documented physical state.
- Observed: telemetry/OLT association/power/alarm state with collection timestamp and freshness.

Observed data never silently overwrites documented passive connectivity.

## Frontend rules

- Preserve the CyberSathy FiberNet visual language in `docs/03-ui-ux-screenbook.md`.
- Desktop: dark navy sidebar, light work area, contextual right panel, data-dense but readable tables.
- Mobile: PWA, bottom navigation, large touch targets, offline/stale indicators.
- Every significant page has loading, empty, error, permission-denied, stale, unknown, and conflict states where applicable.
- Color is never the only signal; use labels/icons/patterns.
- Saving diagram layout is separate from saving topology connectivity.
- Moving a map point does not reconnect fibers.
- Moving a topology node changes layout only.

## Backend rules

Use a modular monolith initially. Recommended modules are identity/tenancy, locations, inventory, olt, cables, connectivity, topology, optical, customers, observations, changes, reservations, incidents, work orders, measurements, imports/exports, reports, integrations, attachments, and audit.

PostgreSQL/PostGIS is authoritative. Do not add a second authoritative graph database in the initial implementation.

All tenant domain tables must contain tenant ownership or be reachable through an enforced tenant-owned relation. Apply backend authorization to object reads, writes, exports, jobs, and attachment access.

## API rules

- Base path: `/api/v1/`.
- Authenticated tenant context is required.
- Write connections using endpoint UUIDs and typed connection semantics, not cable names/colors.
- Use stable machine-readable error codes plus human-readable explanations, affected IDs, and remediation hints.
- Idempotency keys are required for change creation, import commits, field synchronization, and other retry-sensitive operations.
- Paginate large lists. Use viewport/spatial map queries. Do not load every fiber/ONU on first map render.

## No-placeholder policy

Do not claim a feature is implemented because a screen exists. A feature is implemented only when:

1. the domain model persists it,
2. backend validation enforces relevant rules,
3. API behavior is functional,
4. the UI is connected to the API,
5. the applicable tests pass.

Unavailable integrations must be visibly marked unavailable or disabled.

## Phase policy

Implement in the order documented in `docs/16-implementation-roadmap.md`. Preserve the complete domain model from Phase 1 so later operational workflows do not require replacing the topology model.

## Acceptance gates

A01-A30 in `acceptance/acceptance-matrix.md` are contractual behavior. Add tests for unique loss counting, reservation expiry, restoration, import retries, source mismatch reconciliation, permissions, and offline conflict behavior.

Before reporting a phase complete:

- run domain/unit tests,
- run PostgreSQL transactional tests,
- run API tests,
- run relevant browser/UI tests,
- run tenant isolation tests,
- demonstrate scenario seed traces,
- verify persistence across restart,
- report exact implemented/deferred requirements and known limitations.

## Demo-data rule

Use synthetic records and fictional/demo coordinates. Never imply demonstration coordinates, power readings, customer references, or serial numbers are actual surveyed production data.

## Scope boundary

The application documents, plans, validates, traces, calculates, reconciles, and manages work. Initial scope does not execute device configuration writes or automatic ONU provisioning.
