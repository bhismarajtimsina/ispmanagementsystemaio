# Product Vision and Boundaries

FiberNet is designed to operate an ISP from commercial onboarding through physical fiber, access authentication, customer billing, network monitoring and field repair. It is not a single monolithic state machine. The platform uses explicit bounded contexts with APIs and events between them.

## Product pillars
1. CyberSathy SaaS control plane for Superadmin, subscriptions, tenant creation, module entitlements and driver governance.
2. ISP and reseller OSS/BSS for customers, packages, invoices, wallets, collections, RADIUS/AAA, PPPoE and HotSpot.
3. NMS for routers, switches, OLTs, ONUs, servers, interfaces, links, alarms, events, metrics, topology and configuration lifecycle.
4. Fiber GIS/ODN for exact passive optical connectivity, splice history, optical engineering, OTDR and customer path trace.
5. CPE management with TR-069/ACS and TR-369/USP.
6. Field operations, incidents, tickets, work orders and inventory.

## Explicit non-goals for initial releases
- Claiming universal configuration-write compatibility across all vendors.
- Inferring undocumented splices from geometry.
- Allowing raw user-provided CLI without validation and authorization.
- Mixing subscriber billing status with physical fiber truth.
