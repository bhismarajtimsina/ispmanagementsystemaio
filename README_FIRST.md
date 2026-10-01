# CyberSathy FiberNet — Complete Documentation Archive

Prepared: 2026-10-01

This archive consolidates the full FiberNet documentation produced in this project.

## Contents

1. `01_Current_Enterprise_Documentation/`
   - Primary source of truth for current implementation planning.
   - 5,551 atomic feature specification pages plus architecture/product books.
   - Includes `CLAUDE.md`, master manifest, menu tree, API outline, security, roles, vendor capability templates, architecture diagrams, runbooks, tests and UI references.

2. `02_Legacy_Documentation/`
   - Earlier master system report and developer documentation retained for reference.

3. `03_UI_Mockups/`
   - All current-conversation FiberNet UI mockups, including Superadmin, ISP Admin, Reseller, Fiber GIS, topology, OLT/PON, ONT/ONU, TR-069/ACS, alarms, work orders, OTDR and related views.

4. `04_Source_Utilities/`
   - Documentation generation utility retained for reproducibility where available.

## Implementation authority

For new development, read in this order:

1. `01_Current_Enterprise_Documentation/CLAUDE.md`
2. `01_Current_Enterprise_Documentation/README.md`
3. `01_Current_Enterprise_Documentation/reference/architecture-principles.md`
4. `01_Current_Enterprise_Documentation/reference/complete-menu-feature-catalog.md`
5. `01_Current_Enterprise_Documentation/reference/menu-tree.json`
6. Relevant module books / atomic requirements.

The canonical fiber topology remains the physical termination/connection graph. Map lines, topology-diagram edges, telemetry observations and billing state must not silently replace physical connectivity.
