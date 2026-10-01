# Tenancy, Superadmin, ISP and Reseller Model

The platform hierarchy supports CyberSathy Superadmin, ISP tenants, reseller/sub-reseller organizations and end customers. Every domain record is tenant-scoped. Parent/child organizations allow wholesale and reseller business models without leaking data between siblings.

## Permission equation
Actual permission = platform entitlement ∩ tenant module entitlement ∩ role permission ∩ region/device scope ∩ object policy.

## Superadmin responsibilities
Superadmin governs subscription plans, feature flags, quotas, vendor/device catalogs, driver versions, firmware repositories, global parameter dictionaries, ACS/USP platform services, platform RADIUS services, integrations and audited support access.

## ISP responsibilities
ISP administrators manage actual devices, customers, billing, RADIUS services, network topology, fiber assets, work orders and tenant configuration within Superadmin constraints.

## Reseller responsibilities
Reseller access is permission-driven. A reseller may have only commercial tools, or may additionally receive scoped fiber maps, OLT/ONU visibility, ONU registration and field work functions for assigned areas.
