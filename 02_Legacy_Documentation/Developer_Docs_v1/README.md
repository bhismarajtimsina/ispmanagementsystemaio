# CyberSathy FiberNet - ISP Fiber Mapping and ODN Management

Version: 1.0
Prepared for: CyberSathy IT and Technology
Date: 30 September 2026

CyberSathy FiberNet is a production-oriented ISP fiber mapping, optical distribution network documentation, tracing, maintenance, planning, and troubleshooting platform.

The central product is not a map drawing tool. The source of truth is a tenant-isolated physical connectivity database containing cable segments, individual fibers, fiber ends, passive component ports, optical transfer paths, splices, patches, continuities, OLT PON ports, ONU optical ports, revisions, measurements, and operational observations.

## Documentation map

- `CLAUDE.md` - repository instructions for AI-assisted implementation.
- `docs/01-product-and-scope.md` - product goals, terminology, boundaries, and system principles.
- `docs/02-feature-catalog.md` - complete functional feature catalog and phases.
- `docs/03-ui-ux-screenbook.md` - menu tree, page-by-page UI behavior, interaction states, responsive behavior.
- `docs/04-frontend-architecture.md` - React/TypeScript structure, routing, state, components, map/topology implementation.
- `docs/05-backend-architecture.md` - Django/DRF modular monolith and domain services.
- `docs/06-data-model-and-topology.md` - canonical physical graph, entities, invariants, revisions, indexing.
- `docs/07-api-contract.md` - versioned API behavior, errors, concurrency, idempotency.
- `docs/08-optical-engineering.md` - deterministic loss ledger and optical power calculations.
- `docs/09-change-management.md` - planning, reservations, approval, field execution, commissioning, history.
- `docs/10-faults-field-operations.md` - incidents, impact, repair, work orders, PWA/offline workflows, OTDR.
- `docs/11-security-multitenancy.md` - tenant isolation, RBAC, audit, attachments, secrets, security tests.
- `docs/12-import-export-integrations.md` - CSV/XLSX/GIS import, topology JSON, read-only OLT adapters, reconciliation.
- `docs/13-testing-and-quality.md` - unit/integration/UI/performance testing and A01-A30 mapping.
- `docs/14-deployment-and-operations.md` - environments, containers, workers, backups, observability, disaster recovery.
- `docs/15-demo-data.md` - synthetic Nepal demo dataset and fixtures.
- `docs/16-implementation-roadmap.md` - build sequence, milestones, definition of done.
- `docs/17-repository-structure.md` - recommended monorepo structure and module ownership.
- `docs/18-nonfunctional-requirements.md` - performance, accessibility, localization, reliability, privacy.
- `docs/19-glossary.md` - fiber/ODN/application terminology.
- `architecture/*.mmd` - Mermaid architecture and topology diagrams.
- `api/openapi-outline.yaml` - OpenAPI-oriented endpoint outline for implementation.
- `acceptance/acceptance-matrix.md` - acceptance-test traceability matrix.

## Non-negotiable system rules

1. Map geometry is not optical connectivity.
2. A normal splice connects exactly two eligible terminations and cannot branch.
3. Branching requires an explicit splitter/coupler transfer model.
4. One PON port feeding two fibers is represented by a physical splitter, not two independent PON sources.
5. Fiber identity is cable segment + fiber number + UUID; color is descriptive only.
6. Blue-to-red repair is an explicit splice/path change and never a color rename.
7. Mid-span uncut fibers are continuity, with no fictitious splice loss.
8. The commissioned active service path has one upstream PON root.
9. Closed active passive optical loops and conflicting PON sources are rejected.
10. Drafts may be incomplete; commissioned topology may not falsely pass incomplete validation.
11. Optical calculations are backend-authoritative and provenance-aware.
12. Planned, as-built, and observed operational state remain separate.
13. Commissioning validation and commit occur atomically under concurrency control.
14. Historical as-built revisions are immutable.
15. Every domain record is tenant-owned and authorization is enforced server-side.
