# FiberNet Enterprise Documentation Library

Version 3.0 - CyberSathy IT and Technology

This library defines FiberNet as a multi-tenant ISP OSS/BSS + NMS + AAA + ACS/USP + Fiber GIS/ODN + automation platform. The source of truth is deliberately split by domain: billing owns financial state, AAA owns access policy, NMS owns observed telemetry, device configuration owns intended active-device state, Fiber GIS owns passive physical connectivity, and audit/revisions preserve history.

## Documentation rules
- No map crossing creates connectivity.
- No observed OLT/ONU association silently overwrites documented fiber topology.
- No configuration write is considered successful until read-back/verification where supported.
- No tenant can access another tenant's data or device secrets.
- Unsupported vendor capabilities remain visibly unavailable rather than emulated.
- Planned, documented as-built and observed operational state are independent.
- Configuration, topology and billing changes are auditable.

## Audience
Product, engineering, NOC, fiber teams, billing teams, field operations, security, QA, DevOps and AI coding agents.

See `MASTER-MANIFEST.csv` for the complete page registry and `ai/CLAUDE.md` for implementation instructions.
