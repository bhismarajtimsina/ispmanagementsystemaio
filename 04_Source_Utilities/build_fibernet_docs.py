from pathlib import Path
import csv, json, shutil, textwrap, zipfile, hashlib, os, re
from datetime import date

OUT = Path('/mnt/data/FiberNet_Enterprise_Documentation_v3')
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for d in ['books','requirements','ui/mockups','architecture','api','schemas','matrices','runbooks','tests','examples','ai','reference']:
    (OUT/d).mkdir(parents=True, exist_ok=True)

# ---------- product taxonomy ----------
roles = [
    'CyberSathy Superadmin','Platform Support Engineer','ISP Owner','ISP Administrator','NOC Operator',
    'Network Engineer','Fiber Engineer','Billing Officer','Customer Support Agent','Field Technician',
    'Reseller Owner','Reseller Staff','Customer','Auditor','API Client'
]

modules = {
'Superadmin Platform': [
    'Platform Dashboard','Organizations','Create ISP','Create Reseller','Organization Tree','Pending Approvals',
    'Suspended Organizations','Organization Templates','Plans & Packages','Tenant Subscriptions','Module Entitlements',
    'Device Limits','ONU Limits','Customer Limits','Storage Limits','API Limits','Trial Management','Renewals',
    'SaaS Invoices','Subscription History','Module Registry','Feature Flags','Tenant Overrides','Beta Features',
    'Dependency Matrix','Platform Users','Roles & Permissions','Tenant Access','Sessions','API Tokens','Announcements',
    'Platform Settings','System Health','Integrations','Audit Logs','Backup & Restore'
],
'Device Platform': [
    'Vendors','Device Families','Device Models','Capability Matrix','Protocol Profiles','Driver Registry','Driver Versions',
    'Command Templates','Response Parsers','API Mappings','SNMP Templates','SNMP OID Catalog','Syslog Parsers','Trap Mappings',
    'Backup Templates','Configuration Templates','Firmware Repository','Firmware Compatibility','Driver Test Laboratory',
    'Unknown Device Queue','Tenant Driver Assignment','Credential Policies','Secret References','Read-only Capability',
    'Write Capability','Configuration Risk Levels','Device Discovery','Inventory Reconciliation','Lifecycle Management'
],
'OLT Platform': [
    'OLT Vendors','OLT Models','Chassis Templates','Board Templates','Slot Rules','PON Technologies','PON Port Models',
    'Optical Profiles','ONU Authentication Methods','Line Profiles','Service Profiles','DBA Profiles','T-CONT Templates',
    'GEM Templates','VLAN Templates','Service Port Templates','OMCI Profiles','OLT TR-069 Profiles','Registration Workflows',
    'Polling Templates','Alarm Definitions','Provisioning Commands','OLT Discovery','Board Discovery','PON Discovery',
    'Configuration Backup','Configuration Diff','Firmware Compatibility','Optical Thresholds','OLT Performance'
],
'ONT / ONU Platform': [
    'ONT Vendors','ONT Models','Capability Profiles','Ethernet Ports','Wi-Fi Capabilities','Voice Capabilities','WAN Capabilities',
    'TR-069 Data Models','USP Data Models','OMCI Capabilities','Registration Templates','Firmware','Compatibility Matrix',
    'ONU Discovery','ONU Registration','Serial Authentication','LOID Authentication','Password Authentication','ONU ID Allocation',
    'ONU Replacement','ONU Migration','Optical Monitoring','Distance Monitoring','Dying Gasp','LOS Handling','Config State',
    'Match State','Service Association','Customer Association','ONU History','ONU Diagnostics'
],
'TR-069 / ACS': [
    'ACS Dashboard','ACS Servers','ACS Clusters','ACS Connection Settings','ACS Authentication','TLS Certificates',
    'Parameter Dictionary','Vendor Parameter Mappings','TR-098 Mapping','TR-181 Mapping','Vendor Extensions',
    'Provisioning Templates','Template Inheritance','Auto-Provision Rules','Firmware Jobs','Configuration Jobs','Inform Events',
    'Connection Requests','Diagnostics','Failed Jobs','ACS Logs','Security','Device Discovery','Unknown CPE Queue','Periodic Inform',
    'Inform Retry Policy','Task Queue','Read-back Verification','Parameter Explorer','GetParameterValues','SetParameterValues',
    'Download RPC','Upload RPC','Reboot RPC','Factory Reset Policy','Configuration Download','Firmware Rollout','Canary Deployment'
],
'USP / TR-369': [
    'USP Dashboard','USP Controllers','USP Agents','MTP Profiles','MQTT Profiles','WebSocket Profiles','Parameter Models',
    'Event Subscriptions','Operations','Commands','USP Security','Certificate Management','Agent Discovery','Managed Wi-Fi',
    'Telemetry','Bulk Data Collection','USP Provisioning','USP Diagnostics','USP History'
],
'ISP CRM': [
    'Customer Dashboard','All Customers','Leads','New Applications','Feasibility Checks','Connections','Active Customers',
    'Suspended Customers','Terminated Customers','KYC','Documents','Customer Locations','Customer Services','Multiple ONUs',
    'Relocation','Package Upgrade','Package Downgrade','Suspension','Reactivation','Termination','Customer Notes','Customer History',
    'Coverage Map','Customer Tags','Bulk Customer Actions','Customer Import','Customer Export'
],
'Billing & Finance': [
    'Billing Dashboard','Invoices','Recurring Billing','Pro-Rata Billing','Payments','Due Bills','Packages','Plan Pricing',
    'Taxes','Discounts','Coupons','Credits','Debit Notes','Credit Notes','Refunds','Deposits','Installation Fees','Hardware Charges',
    'Wallet','Collection','Payment Gateways','Cash Collection','Bank Payments','Mobile Wallet Payments','Aging Report',
    'Automatic Suspension','Automatic Restoration','Payment Reminders','Financial Reports','Revenue Analytics','Reseller Settlement'
],
'Reseller Management': [
    'Reseller Dashboard','Reseller Customers','Reseller Packages','Wholesale Pricing','Reseller Wallet','Wallet Top-up',
    'Reseller Commissions','Commission Rules','Reseller Payments','Reseller Invoices','Reseller PPPoE','Reseller HotSpot',
    'Reseller Vouchers','Reseller Sessions','Reseller Tickets','Reseller Work Orders','Reseller Reports','Reseller Staff',
    'Reseller Network Scope','Reseller Fiber Map','Reseller OLT View','Reseller ONU Registration','Reseller Permissions'
],
'RADIUS / AAA': [
    'AAA Dashboard','RADIUS Clusters','RADIUS Users','RADIUS Groups','RADIUS Profiles','RADIUS Attributes','Vendor Dictionaries',
    'NAS Devices','Active Sessions','Authentication Logs','Accounting Logs','Accounting Interim Updates','CoA','Disconnect Request',
    'Framed IP','IPv6 Prefix Delegation','IP Pool Policy','Session Timeout','Idle Timeout','Simultaneous Use','Bandwidth Policy',
    'FUP Policy','Expiration Policy','Suspension Policy','Restoration Policy','RADIUS Health','RADIUS Replication','RADIUS Audit'
],
'PPPoE': [
    'PPPoE Dashboard','PPPoE Users','PPPoE Profiles','PPPoE Servers','PPPoE Sessions','PPPoE IP Pools','Static IP Assignment',
    'IPv6 Assignment','PPPoE NAS Mapping','Failed Authentication','Session History','Usage Accounting','Rate Changes','Disconnect',
    'Bulk Disconnect','Profile Migration','PPPoE Reports','PPPoE Alarms'
],
'HotSpot': [
    'HotSpot Dashboard','HotSpot Servers','HotSpot Users','HotSpot Profiles','HotSpot Sessions','Vouchers','Voucher Batches',
    'Voucher Printing','Captive Portal','Portal Branding','MAC Authentication','OTP Integration','Walled Garden','IP Bindings',
    'Cookies','Data Quotas','Speed Limits','Validity','HotSpot Zones','RADIUS Integration','HotSpot Revenue','HotSpot Reports'
],
'NMS': [
    'NMS Dashboard','Device Inventory','Routers','Switches','Firewalls','Servers','Wireless APs','UPS/PDU','Interfaces','Links',
    'Sites','POPs','Racks','Device Health','CPU Monitoring','Memory Monitoring','Storage Monitoring','Temperature Monitoring',
    'Voltage Monitoring','Fan Monitoring','Interface Traffic','Interface Errors','CRC Errors','Drops','SFP Diagnostics',
    'Latency','Packet Loss','Jitter','Availability','SLA','Traffic Analytics','95th Percentile','Capacity Planning','Discovery',
    'LLDP Discovery','CDP Discovery','ARP Discovery','MAC Table Discovery','BGP Neighbors','OSPF Neighbors','Route Monitoring',
    'VLAN Monitoring','STP Monitoring','LACP Monitoring','PoE Monitoring','Network Performance','Time-series Retention'
],
'Network Topology': [
    'Topology Dashboard','Physical Topology','Logical Topology','L2 Topology','L3 Topology','Observed Topology','Documented Topology',
    'Planned Topology','Dependency Graph','Path Trace','Link Details','Redundant Links','Link Down Analysis','Root Cause Correlation',
    'Topology History','Topology Diff','Manual Links','Discovered Links','Topology Reconciliation','Impact Analysis'
],
'Fiber GIS / ODN': [
    'Fiber Dashboard','Network Map','Map Layers','Route Editing','Cable Assets','Cable Segments','Fiber Cores','Fiber Ends','Tubes',
    'Closures / JBs','Splice Trays','Splice Editor','Bulk Splice','Mid-span Access','Uncut Continuity','ODF','Patch Panels','Adapters',
    'Pigtails','Patch Cords','Splitters','Couplers','10:90 Coupler','20:80 Coupler','30:70 Coupler','50:50 Splitter','1x2 Splitter',
    '1x4 Splitter','1x8 Splitter','1x16 Splitter','1x32 Splitter','1x64 Splitter','Custom Splitter','Drop Cables','ONU Mapping',
    'PON Root Trace','ONU to OLT Trace','OLT to ONU Tree','Core Trace','Closure Trace','Fiber Reservations','Damaged Core',
    'Blue-to-Red Reroute','Bypass Preview','Optical Budget','Downstream Budget','Upstream Budget','Loss Ledger','Engineering Margin',
    'Overload Check','Reach Check','ONU Count Check','Documentation Completeness','As-built Revisions','Planned Revisions','Observed State',
    'GeoJSON Export','Topology JSON Export','Splice Schedule','Fiber Utilization','Material Estimate','QR Asset Lookup'
],
'OTDR & Measurements': [
    'Measurement Dashboard','Receive Power','Insertion Loss','OTDR Records','OTDR Attachments','OTDR Events','OTDR Candidate Location',
    'Reference Plane','Wavelength','Instrument Registry','Technician','Measurement Quality','Launch Cable Offset','Slack Model',
    'Route Length Calibration','Measurement History','Measured vs Predicted','Loss Trend','OTDR Report','Power Meter Report'
],
'Alarms & Events': [
    'Alarm Dashboard','Active Alarms','Cleared Alarms','Event Logs','Critical Alarms','Major Alarms','Minor Alarms','Warnings',
    'Device Down','Interface Down','Link Flap','OLT Down','PON Down','ONU LOS','Dying Gasp','Low RX','High RX','High CPU',
    'High Memory','High Temperature','Voltage Alarm','Fan Alarm','BGP Down','OSPF Down','RADIUS Failure','TR-069 Offline',
    'Config Change','Alarm Acknowledgement','Alarm Assignment','Alarm Escalation','Alarm Deduplication','Alarm Suppression',
    'Correlation Rules','Dependency Rules','Root Cause','Alarm Notifications','Alarm History','Alarm Reports'
],
'Incidents & Work Orders': [
    'Incident Dashboard','Incidents','Fault Scope','Affected Services','Probable Root Cause','RCA','Incident Timeline',
    'Work Orders','Installation Work Order','Fault Repair','Fiber Repair','ONU Replacement','Relocation','Site Survey','Maintenance',
    'Technician Assignment','Field Checklist','Materials','Photos','GPS Evidence','Measurements','Completion Verification',
    'Maintenance Window','Change Link','Related Tickets','Incident Reports','Work Order Reports'
],
'Tickets & Support': [
    'Support Dashboard','Tickets','No Internet','Slow Speed','Wi-Fi Issue','Billing Issue','ONU Issue','Fiber Issue','Relocation Ticket',
    'Package Upgrade Ticket','Ticket SLA','Assignment','Escalation','Internal Notes','Customer Replies','Attachments','Ticket History',
    'Smart Support View','Customer Health Snapshot','Remote Diagnostics','Support Reports'
],
'Inventory': [
    'Inventory Dashboard','Warehouses','Stock Items','Routers Stock','Switches Stock','OLT Stock','Board Stock','SFP Stock','ONU Stock',
    'Fiber Stock','Closure Stock','Splitter Stock','Patch Cord Stock','Pigtail Stock','Tools','Consumables','Serial Tracking','Warranty',
    'Stock Transfer','Technician Stock','Customer Issued','Returns','Repairs','Retired Assets','Procurement','Low Stock Alerts','Inventory Reports'
],
'Configuration & Automation': [
    'Configuration Dashboard','Running Config','Startup Config','Config Backup','Scheduled Backup','Config Versions','Config Diff',
    'Configuration Templates','Proposed Config','Dry Run','Validation','Approval','Maintenance Windows','Config Push','Read-back Verification',
    'Rollback','Automation Workflows','Triggers','Scheduled Jobs','Event Actions','Approval Policies','Validation Rules','Automation History',
    'Job Queue','Failed Jobs','Retry Policies','Idempotency','Change Set','Topology Revision','Audit Trail'
],
'IPAM & Addressing': [
    'IPAM Dashboard','IPv4 Networks','IPv6 Networks','Subnets','Prefixes','IP Pools','Public IPs','Private IPs','Static Assignments',
    'Dynamic Assignments','Reserved IPs','Customer IPs','Management IPs','NAS IPs','Gateways','VRFs','VLAN Registry','Address Conflicts',
    'Pool Exhaustion','IP History','IP Reports'
],
'Reports & Analytics': [
    'Report Center','Financial Reports','Customer Reports','RADIUS Reports','PPPoE Reports','HotSpot Reports','Traffic Reports',
    'NMS Reports','OLT Reports','ONU Reports','Optical Reports','Fiber Reports','Inventory Reports','Work Order Reports','Ticket Reports',
    'SLA Reports','Utilization Reports','Capacity Reports','Audit Reports','Scheduled Reports','Report Export','Custom Reports'
],
'Customer Portal': [
    'Customer Dashboard','My Internet','My Package','Usage','Invoices','Payments','Wallet','Upgrade Package','Connection Status','Outages',
    'Tickets','Notifications','Devices','Wi-Fi Settings','ONU Reboot','Profile','Documents','Support','Payment History'
],
'Field PWA': [
    'Field Dashboard','Assigned Work','Offline Packages','Map','Asset Lookup','QR Scanner','GPS Capture','Closure Lookup','Splice Schedule',
    'Photo Capture','Measurement Entry','OTDR Entry','Proposed Changes','Offline Queue','Sync Conflicts','Material Usage','Checklist',
    'Technician Notes','Completion Submission','Last Sync','Cache Expiry'
],
'Administration & Security': [
    'Tenant Settings','Branding','Domains','Timezone','Currency','Localization','Staff','Teams','Regions','Roles','Permissions',
    'MFA','Session Policy','Password Policy','IP Allowlist','API Keys','Webhooks','Secret Management','Attachment Security',
    'Audit','Export Audit','Login Audit','Device Action Audit','Retention','Backups','Restore Tests','Data Privacy','Rate Limits'
],
'APIs & Integrations': [
    'API Authentication','API Versioning','Pagination','Filtering','Idempotency','Error Model','Webhooks','Payment Gateway Adapter',
    'SMS Adapter','Email Adapter','CRM Adapter','Accounting Adapter','Vendor Device Adapter','OLT Adapter','Router Adapter','Switch Adapter',
    'Object Storage Adapter','Map Provider Adapter','RADIUS Integration','ACS Integration','USP Integration','Import API','Export API',
    'OpenAPI','SDK Strategy','API Audit','Integration Health'
],
'Quality & Operations': [
    'Testing Strategy','Unit Tests','Domain Tests','Transactional Tests','API Tests','UI Tests','Accessibility Tests','Security Tests',
    'Tenant Isolation Tests','Performance Tests','Load Tests','Chaos Tests','Backup Restore Tests','Upgrade Tests','Driver Contract Tests',
    'Acceptance Tests','Release Process','Feature Flags','Migration Strategy','Deployment','High Availability','Disaster Recovery',
    'Observability','Logging','Metrics','Tracing','SLOs','Runbooks','On-call','Incident Response','Capacity Management'
]
}

# ---------- narrative books ----------
books = {
'00-master-index.md': '''# FiberNet Enterprise Documentation Library\n\nVersion 3.0 - CyberSathy IT and Technology\n\nThis library defines FiberNet as a multi-tenant ISP OSS/BSS + NMS + AAA + ACS/USP + Fiber GIS/ODN + automation platform. The source of truth is deliberately split by domain: billing owns financial state, AAA owns access policy, NMS owns observed telemetry, device configuration owns intended active-device state, Fiber GIS owns passive physical connectivity, and audit/revisions preserve history.\n\n## Documentation rules\n- No map crossing creates connectivity.\n- No observed OLT/ONU association silently overwrites documented fiber topology.\n- No configuration write is considered successful until read-back/verification where supported.\n- No tenant can access another tenant's data or device secrets.\n- Unsupported vendor capabilities remain visibly unavailable rather than emulated.\n- Planned, documented as-built and observed operational state are independent.\n- Configuration, topology and billing changes are auditable.\n\n## Audience\nProduct, engineering, NOC, fiber teams, billing teams, field operations, security, QA, DevOps and AI coding agents.\n\nSee `MASTER-MANIFEST.csv` for the complete page registry and `ai/CLAUDE.md` for implementation instructions.''',
'01-product-vision-and-boundaries.md': '''# Product Vision and Boundaries\n\nFiberNet is designed to operate an ISP from commercial onboarding through physical fiber, access authentication, customer billing, network monitoring and field repair. It is not a single monolithic state machine. The platform uses explicit bounded contexts with APIs and events between them.\n\n## Product pillars\n1. CyberSathy SaaS control plane for Superadmin, subscriptions, tenant creation, module entitlements and driver governance.\n2. ISP and reseller OSS/BSS for customers, packages, invoices, wallets, collections, RADIUS/AAA, PPPoE and HotSpot.\n3. NMS for routers, switches, OLTs, ONUs, servers, interfaces, links, alarms, events, metrics, topology and configuration lifecycle.\n4. Fiber GIS/ODN for exact passive optical connectivity, splice history, optical engineering, OTDR and customer path trace.\n5. CPE management with TR-069/ACS and TR-369/USP.\n6. Field operations, incidents, tickets, work orders and inventory.\n\n## Explicit non-goals for initial releases\n- Claiming universal configuration-write compatibility across all vendors.\n- Inferring undocumented splices from geometry.\n- Allowing raw user-provided CLI without validation and authorization.\n- Mixing subscriber billing status with physical fiber truth.\n''',
'02-tenancy-superadmin-reseller.md': '''# Tenancy, Superadmin, ISP and Reseller Model\n\nThe platform hierarchy supports CyberSathy Superadmin, ISP tenants, reseller/sub-reseller organizations and end customers. Every domain record is tenant-scoped. Parent/child organizations allow wholesale and reseller business models without leaking data between siblings.\n\n## Permission equation\nActual permission = platform entitlement ∩ tenant module entitlement ∩ role permission ∩ region/device scope ∩ object policy.\n\n## Superadmin responsibilities\nSuperadmin governs subscription plans, feature flags, quotas, vendor/device catalogs, driver versions, firmware repositories, global parameter dictionaries, ACS/USP platform services, platform RADIUS services, integrations and audited support access.\n\n## ISP responsibilities\nISP administrators manage actual devices, customers, billing, RADIUS services, network topology, fiber assets, work orders and tenant configuration within Superadmin constraints.\n\n## Reseller responsibilities\nReseller access is permission-driven. A reseller may have only commercial tools, or may additionally receive scoped fiber maps, OLT/ONU visibility, ONU registration and field work functions for assigned areas.\n''',
'03-frontend-design-system.md': '''# Frontend Design System\n\nThe FiberNet UI uses a desktop-first NOC workspace and an installable field PWA. Desktop follows a three-region pattern: persistent dark navigation, primary work canvas and optional context/detail panel.\n\n## Visual language\n- Navy navigation shell.\n- CyberSathy blue primary actions.\n- Green healthy/online.\n- Orange degraded/warning.\n- Red critical/down/damaged.\n- Purple passive optical components.\n- Gray unknown/stale/disabled.\n- Icons, text and patterns accompany color.\n\n## Screen states\nEvery screen must define loading, empty, success, partial, unknown, stale, warning, error, permission-denied, offline and conflict states.\n\n## Shared components\nGlobalSearch, TenantSwitcher, AssetStatus, EntityDrawer, VirtualizedTable, MapLayerControl, TopologyCanvas, TraceTimeline, LossLedger, OpticalResult, DiffViewer, AuditTimeline, WorkOrderCard, MetricCard, AlertBadge, PermissionGate and EntitlementGate.\n''',
'04-superadmin-ui-book.md': '''# Superadmin UI Book\n\nThe Superadmin interface is a distinct control plane. Its menu exposes Organizations, Subscriptions, Module Control, Device Platform, OLT Platform, ONT/ONU Platform, TR-069/ACS, USP, AAA platform, monitoring platform, automation, integrations, users/access, platform operations, audit/security and system settings.\n\nThe dashboard shows organizations, customers, ONUs, network devices, monthly recurring revenue, active alarms, organization growth, subscription status, driver health, ACS inform rate, failed provisioning, RADIUS health, collector health, unknown models and firmware rollout state.\n\nA Superadmin may enter a tenant through time-bound audited support access. Impersonation must display a persistent banner and generate audit events.\n''',
'05-isp-admin-ui-book.md': '''# ISP Admin UI Book\n\nThe ISP dashboard combines commercial and network operation data without collapsing their authorities. Header-to-footer modules include customers, billing, RADIUS/AAA, PPPoE, HotSpot, Network, Fiber, Monitoring, OLT/ONU, TR-069/USP, Alarms, Faults, Work Orders, Tickets, Inventory, Reports and Administration.\n\nThe home page presents customer/session/ONU/device/revenue/ticket/alarm KPIs, live topology, traffic, customer growth, OLT health, top ONU issues, RADIUS sessions, tickets, payments and system health.\n''',
'06-reseller-ui-book.md': '''# Reseller UI Book\n\nReseller menus are generated from entitlements and scope. Commercial-only resellers receive Customers, Billing, Wallet, Packages, PPPoE/Sessions, HotSpot/Vouchers, Tickets, Work Orders, Reports and Staff. Network-enabled resellers additionally receive Fiber Map, Network Topology, scoped Devices, OLTs, ONUs/ONTs, Links, IPAM and Alarms.\n\nThe reseller dashboard must show only assets and customers assigned to the reseller hierarchy or geographic/network scope. Fiber mapping remains the same canonical physical model as the ISP view; it is filtered, not copied.\n''',
'07-customer-portal-ui-book.md': '''# Customer Portal UI Book\n\nThe customer portal exposes only safe self-service capabilities: current package, invoices, payments, usage, connection status, outages, tickets, notifications, devices and permitted Wi-Fi controls. Reboot may be available if policy allows. VLAN, PON, OLT, RADIUS attributes and infrastructure data are never exposed directly.\n''',
'08-nms-architecture.md': '''# NMS Architecture\n\nNMS uses distributed collectors near managed networks. Collectors perform SNMPv3, ICMP, syslog/trap ingestion, REST/NETCONF/SSH/vendor API calls and supported streaming telemetry. They publish normalized inventory, metrics and events to the central platform over authenticated encrypted channels.\n\nMetrics belong in a time-series store; business/topology metadata belongs in PostgreSQL/PostGIS. Redis supports caching and jobs. Device credentials are references into a secret store.\n\nObserved topology is derived from LLDP/CDP, MAC/ARP tables and routing adjacencies, then reconciled against documented topology. Discovery never overwrites human-maintained authoritative links without review.\n''',
'09-device-driver-framework.md': '''# Device Driver Framework\n\nDrivers implement a capability contract rather than scattering vendor conditionals through the application. A driver declares identity/firmware compatibility, read capabilities, write capabilities, schemas, command/API mappings, response parsers, monitoring metrics, normalized alarms and verification methods.\n\nUnsupported capabilities return an explicit unsupported result. Firmware-specific parser and command versions are immutable once published. Superadmin assigns stable/beta driver versions to tenants.\n''',
'10-olt-ont-provisioning.md': '''# OLT and ONT Provisioning\n\nOLT provisioning is model and firmware aware. Device definitions include chassis, boards, PON technologies, authentication methods, line profiles, service profiles, DBA, T-CONT, GEM, VLAN, service-port and OMCI capabilities.\n\nONU registration workflow: discover -> classify model -> validate serial/LOID -> allocate ONU ID -> select profiles -> register -> configure management/service paths -> configure TR-069/USP where applicable -> read back -> optical validation -> customer association -> audit.\n\nThe platform must distinguish documented configuration from observed OLT state and surface mismatches.\n''',
'11-tr069-acs.md': '''# TR-069 / ACS\n\nACS is tenant isolated while using shared platform infrastructure. Device identity includes OUI, ProductClass, serial, manufacturer, hardware/software version and data model family. Unknown devices enter a classification queue.\n\nFiberNet normalizes generic settings such as SSID or WAN configuration to model/firmware-specific TR-098/TR-181/vendor-extension parameter paths. Provisioning tasks have queued, waiting, sent, acknowledged, applying, verified, success, failed, expired and cancelled states.\n\nA SetParameterValues response is not sufficient proof of success when read-back verification is available. Firmware jobs support canary rollout, staged percentages and automatic halt thresholds.\n''',
'12-usp.md': '''# TR-369 / USP\n\nUSP support is a separate controller capability with MTP profiles such as MQTT and WebSocket where supported. It covers parameter access, operations, event subscriptions, telemetry, managed Wi-Fi and device lifecycle. TR-069 and USP may coexist during migration; ownership policies prevent competing controllers from repeatedly overwriting the same settings.\n''',
'13-radius-pppoe-hotspot.md': '''# RADIUS, PPPoE and HotSpot\n\nThe AAA plane centralizes authentication, authorization and accounting using a FreeRADIUS-compatible service. Tenant policies generate vendor attributes and bandwidth authorization. Accounting records are immutable operational evidence and feed usage reports, but invoices remain owned by Billing.\n\nPPPoE supports credentials, profiles, pools, static addresses, IPv6 delegation, session monitoring, CoA/disconnect and history. HotSpot supports users, vouchers, captive portals, quotas, validity, MAC authentication, walled garden and reseller allocation.\n''',
'14-billing-crm-reseller.md': '''# Billing, CRM and Reseller Commerce\n\nBilling supports recurring prepaid/postpaid plans, prorating, taxes, discounts, credits/debits, deposits, installation/hardware charges, wallets, collections and payment integrations. Automatic suspension/restoration is policy-driven and executed through AAA, not ad-hoc router changes.\n\nCustomer lifecycle spans lead, application, feasibility, reservation, work order, installation, ONU registration, AAA activation, billing activation, active service, changes and termination.\n\nResellers support commission, wholesale and wallet models with hierarchical package pricing and separate margin reporting.\n''',
'15-fiber-gis-topology.md': '''# Fiber GIS and Passive Optical Topology\n\nPostgreSQL/PostGIS is the source of truth for passive topology. Fiber spans, termination nodes, splices, continuity, component transfer paths, patching and ONU/PON terminations are explicit. Geographic geometry is not connectivity.\n\nThe system supports arbitrary core counts, repeated colors across tubes, 10:90/20:80/30:70 couplers, equal splitters, mid-span access, uncut continuity, blue-to-red reroutes, ODFs, adapters and revision history.\n\nTrace states include complete, incomplete, ambiguous, invalid loop, blocked by known damage, incompatible component and unknown optical budget.\n''',
'16-optical-engineering.md': '''# Optical Engineering\n\nOptical calculations are deterministic backend services with a component loss ledger. Every input carries provenance: manufacturer rated, measured, project default or ideal estimate. Datasheet total insertion loss must not be combined with ideal split loss a second time. Downstream and upstream budgets are calculated separately by wavelength and transmitter/receiver profile.\n\nThe result exposes predicted power, weakest/strongest cases, sensitivity headroom, overload headroom, engineering margin remaining, reach and ODN constraints, missing data and calculation revision.\n''',
'17-alarms-events-incidents.md': '''# Alarms, Events and Incidents\n\nRaw device events are normalized by a global alarm dictionary. Alarm rules add severity, thresholds, deduplication windows, dependencies and notification policies. Correlation can group downstream symptoms under a likely root event, such as suppressing thousands of ONU-offline alarms when an OLT uplink is down.\n\nIncidents remain hypotheses until confirmed. They track scope, services, root cause evidence, assignments, work orders, timeline and RCA.\n''',
'18-workorders-field.md': '''# Work Orders and Field Operations\n\nWork orders include exact assets, fiber/core labels, existing/proposed splice instructions, materials, affected services, GPS, photos, measurements, checklist and required evidence. Offline field packages are drafts with idempotency keys and base topology revisions. Conflicting offline occupancy changes require review; last-write-wins is prohibited.\n''',
'19-inventory.md': '''# Inventory and Asset Lifecycle\n\nInventory distinguishes stock from installed topology. Serialized assets such as routers, switches, OLT boards, SFPs and ONUs maintain warranty and lifecycle. Fiber, closures, splitters, patch components, tools and consumables support warehouse, technician, installed, returned, repair, lost and retired transitions.\n''',
'20-api-and-events.md': '''# API and Event Architecture\n\nAll external APIs are versioned, authenticated and tenant scoped. Write operations support idempotency where retries are expected. 409 is used for stale revision or occupancy conflicts. Validation errors return stable codes, affected IDs and remediation hints.\n\nDomain events use stable names such as device.down, interface.down, onu.los, payment.received, radius.login, workorder.completed and topology.commissioned. Consumers must be idempotent.\n''',
'21-security.md': '''# Security Architecture\n\nSecurity layers include tenant isolation, RBAC/ABAC scope, MFA, secure sessions, TLS, secret vault references, network collectors, least-privilege device credentials, time-limited attachments, audit logs, export controls, rate limits and configuration approval.\n\nDevice write capability is separated from monitoring credentials. Critical configuration and firmware operations can require multi-party approval and a maintenance window.\n''',
'22-data-architecture.md': '''# Data Architecture\n\nPostgreSQL/PostGIS stores tenants, business objects, authoritative topology, revisions and transactional state. A time-series store handles high-cardinality metrics. Redis supports cache and distributed jobs. Object storage keeps photos, documents, config backups, firmware and OTDR files.\n\nEvery domain table carries tenant ownership directly or through an enforced parent. Cross-tenant generic foreign keys are prohibited.\n''',
'23-deployment-ha.md': '''# Deployment, High Availability and Disaster Recovery\n\nProduction separates web/API nodes, background workers, collectors, RADIUS, ACS/USP services, PostgreSQL, Redis, time-series storage and object storage. Health, backups and restoration are tested. Critical services support horizontal scaling where appropriate.\n\nCollectors buffer telemetry during WAN interruption and resume with timestamps rather than pretending the devices were down.\n''',
'24-testing.md': '''# Testing and Acceptance\n\nTesting layers include deterministic domain tests, PostgreSQL transactional tests, API integration tests, UI end-to-end tests, driver contract tests, tenant isolation tests, security tests, performance benchmarks, backup/restore and upgrade tests. The original fiber acceptance cases A01-A30 remain mandatory and are extended by billing, RADIUS, device, ACS and NMS scenarios.\n''',
'25-implementation-roadmap.md': '''# Implementation Roadmap\n\nPhase 1: tenancy, identity, subscription control, customers, billing foundation and canonical fiber topology.\nPhase 2: RADIUS/PPPoE/HotSpot and MikroTik integration.\nPhase 3: distributed NMS collectors, monitoring, topology and alarms.\nPhase 4: OLT/ONU model framework, Huawei adapter first, registration and optical state.\nPhase 5: full Fiber GIS/ODN operational workflows, OTDR and field PWA.\nPhase 6: TR-069/ACS, followed by USP.\nPhase 7: reseller commerce and customer portal.\nPhase 8: configuration automation, approvals and rollback.\nPhase 9: multi-region scale, HA and advanced analytics.\n'''
}

for fn, content in books.items():
    (OUT/'books'/fn).write_text(content.strip()+"\n", encoding='utf-8')

# ---------- architecture diagrams ----------
(OUT/'architecture/system-context.mmd').write_text('''flowchart TB\n  SA[CyberSathy Superadmin] --> CP[Platform Control Plane]\n  CP --> ISP[ISP Tenant]\n  CP --> RES[Reseller Tenant]\n  ISP --> BSS[CRM & Billing]\n  ISP --> AAA[RADIUS / PPPoE / HotSpot]\n  ISP --> NMS[NMS & Automation]\n  ISP --> ACS[TR-069 / USP]\n  ISP --> FIB[Fiber GIS / ODN]\n  NMS --> DEV[Routers / Switches / OLTs / Servers]\n  ACS --> CPE[ONT / CPE]\n  FIB --> CPE\n  BSS --> CUST[Customer Portal]\n''', encoding='utf-8')
(OUT/'architecture/data-authority.mmd').write_text('''flowchart LR\n  Billing[Billing: financial truth] --> Events\n  AAA[AAA: access-policy truth] --> Events\n  NMS[NMS: observed device truth] --> Events\n  Config[Configuration: intended active-device state] --> Events\n  Fiber[Fiber GIS: passive physical truth] --> Events\n  Audit[Audit/Revisions: historical truth]\n  Events --> Audit\n''', encoding='utf-8')
(OUT/'architecture/device-driver.mmd').write_text('''flowchart TB\n  Catalog[Superadmin Device Catalog] --> Model[Vendor / Model / Firmware]\n  Model --> Driver[Versioned Driver]\n  Driver --> Monitor[Monitoring]\n  Driver --> Inventory[Inventory]\n  Driver --> Config[Configuration]\n  Driver --> Alarm[Alarm Normalization]\n  Config --> Verify[Read-back Verification]\n''', encoding='utf-8')
(OUT/'architecture/fiber-topology.mmd').write_text('''flowchart LR\n  PON[PON Port] --> FE[Fiber End]\n  FE --> FS[Fiber Span]\n  FS --> SP[Splice/Continuity]\n  SP --> CP[Component Port]\n  CP --> OT[Optical Transfer]\n  OT --> CP2[Output Port]\n  CP2 --> DROP[Drop Fiber]\n  DROP --> ONU[ONU Optical Port]\n''', encoding='utf-8')

# ---------- AI instructions ----------
claude = '''# CLAUDE.md - FiberNet Enterprise\n\nRead `books/00-master-index.md` and `MASTER-MANIFEST.csv` before changing domain models.\n\n## Non-negotiable architecture\n1. Do not make geographic map edges authoritative connectivity.\n2. Do not let topology diagrams own connectivity.\n3. Passive topology is modeled with typed termination nodes and typed edges in PostgreSQL/PostGIS.\n4. Billing, AAA, NMS, device configuration, ACS/USP and Fiber GIS remain separate bounded contexts.\n5. Every tenant-owned domain object is protected by backend tenant isolation.\n6. Device credentials are secret references, never ordinary asset fields or logs.\n7. Vendor-specific behavior lives in versioned adapters/drivers with capability declarations.\n8. Unsupported capability must return unavailable, never fake success.\n9. Device write jobs require validation, authorization, audit, job state and verification when supported.\n10. Planned, documented-as-built and observed state must remain distinct.\n11. Offline field edits are drafts until server validation/commissioning succeeds.\n12. Stale polling means stale/unknown, not automatically offline.\n\n## Required implementation sequence\nTenancy/identity -> entitlements/permissions -> customers/billing foundation -> authoritative fiber topology -> AAA -> NMS collectors -> device driver framework -> OLT/ONU -> ACS/USP -> field/automation -> scale.\n\n## UI rules\nUse the mockups under `ui/mockups/` as visual references. Preserve consistent sidebar/header/card/table/detail-drawer behavior. All write screens must expose pending/success/failure/conflict states. Color cannot be the only status cue. Large fiber tables must be virtualized.\n\n## Definition of done\nA feature is not implemented because its screen renders. It requires persistence, backend permission checks, tenant isolation, audit where applicable, error states and automated tests.\n'''
(OUT/'ai/CLAUDE.md').write_text(claude, encoding='utf-8')
(OUT/'CLAUDE.md').write_text(claude, encoding='utf-8')

# ---------- reusable requirement generation ----------
category_profiles = {
    'Superadmin Platform': ('platform control plane','CyberSathy Superadmin','platform database'),
    'Device Platform': ('vendor/device abstraction and driver governance','CyberSathy Superadmin, Platform Support Engineer','device catalog and secret references'),
    'OLT Platform': ('OLT model and provisioning framework','CyberSathy Superadmin, Network Engineer','OLT catalog and device configuration state'),
    'ONT / ONU Platform': ('ONU/ONT lifecycle and capability management','Network Engineer, NOC Operator','ONU inventory and observations'),
    'TR-069 / ACS': ('CPE remote management through ACS','Network Engineer, Platform Support Engineer','ACS task, device and parameter stores'),
    'USP / TR-369': ('modern CPE management through USP','Network Engineer, Platform Support Engineer','USP controller state'),
    'ISP CRM': ('subscriber lifecycle management','ISP Administrator, Customer Support Agent','customer and service records'),
    'Billing & Finance': ('financial and recurring service management','Billing Officer, ISP Administrator','billing ledger and invoices'),
    'Reseller Management': ('hierarchical reseller operations','ISP Administrator, Reseller Owner','reseller scoped business records'),
    'RADIUS / AAA': ('central access authentication, authorization and accounting','NOC Operator, Network Engineer','AAA configuration and accounting records'),
    'PPPoE': ('subscriber PPPoE access management','NOC Operator, Network Engineer','AAA and session stores'),
    'HotSpot': ('HotSpot access and voucher management','Reseller Staff, ISP Administrator','HotSpot and AAA records'),
    'NMS': ('network monitoring and observed operational state','NOC Operator, Network Engineer','device inventory plus time-series metrics'),
    'Network Topology': ('active network relationships and dependency analysis','NOC Operator, Network Engineer','documented and observed topology'),
    'Fiber GIS / ODN': ('authoritative passive optical connectivity and geography','Fiber Engineer, Network Engineer','PostgreSQL/PostGIS fiber topology'),
    'OTDR & Measurements': ('field optical measurement evidence','Fiber Engineer, Field Technician','measurement and attachment records'),
    'Alarms & Events': ('normalized operational events and alarms','NOC Operator','alarm/event store'),
    'Incidents & Work Orders': ('fault response and field execution','NOC Operator, Field Technician','incident and work-order records'),
    'Tickets & Support': ('subscriber support case management','Customer Support Agent','ticket records'),
    'Inventory': ('stock and installed asset lifecycle','ISP Administrator, Field Technician','inventory ledger'),
    'Configuration & Automation': ('controlled network changes and repeatable automation','Network Engineer','change/job/config history'),
    'IPAM & Addressing': ('authoritative address and prefix allocation','Network Engineer','IPAM database'),
    'Reports & Analytics': ('derived reporting without changing source data','ISP Administrator, Auditor','report jobs and snapshots'),
    'Customer Portal': ('safe subscriber self-service','Customer','tenant customer portal'),
    'Field PWA': ('offline-capable field operations','Field Technician','offline work package and sync queues'),
    'Administration & Security': ('tenant settings, identity and governance','ISP Administrator, Auditor','identity/security/audit stores'),
    'APIs & Integrations': ('external access and connector contracts','API Client, Platform Support Engineer','API gateway and connector state'),
    'Quality & Operations': ('quality, release and production operations','Platform Support Engineer, Auditor','CI/CD and observability systems')
}

ui_actions = ['view','search','filter','sort','export','open details','compare','refresh','acknowledge','assign','create','edit','validate','submit','approve','execute','retry','cancel']
state_words = ['loading','empty','healthy','warning','critical','unknown','stale','offline','permission-denied','conflict','validation-error','partial-data']

# Specific domain hints
hints = {
 'TR-069 / ACS': ['device identity must include OUI/ProductClass/serial','model/firmware parameter mapping is explicit','tasks are queued and verified','secrets are never rendered in logs'],
 'Fiber GIS / ODN': ['geometry never creates connectivity','fiber identity is segment/core/end UUID based','splices cannot fan out','splitter transfers are explicit and wavelength-aware'],
 'RADIUS / AAA': ['accounting is append-oriented evidence','CoA/disconnect actions are audited','policy changes must be idempotent','billing does not directly edit router customers'],
 'Billing & Finance': ['financial mutations create ledger evidence','automatic suspension is policy-driven','payment reversals are auditable','currency is tenant configurable'],
 'NMS': ['stale telemetry is not equal to down','metric retention is time-series oriented','polling is capability-aware','downstream alarm floods may be correlated'],
 'Configuration & Automation': ['writes require capability support','dry-run/preview precedes high-risk action','read-back verification is preferred','rollback is explicit and never assumed'],
 'Superadmin Platform': ['tenant support access is audited','entitlements are backend enforced','plan limits never rely on UI alone','global template publication is separate from deployment'],
 'OLT Platform': ['commands are model/firmware aware','profiles are not universal across vendors','observed config is reconciled not blindly imported','write capability is driver declared'],
 'ONT / ONU Platform': ['documented source and observed source are separate','registration authentication methods are model aware','replacement preserves history','optical readings carry collection time'],
}

def slug(s):
    s = re.sub(r'[^a-zA-Z0-9]+','-',s.lower()).strip('-')
    return s[:80]

def requirement_page(req_id, module, feature, variant, index):
    purpose, actors, store = category_profiles[module]
    extra = hints.get(module, ['backend authorization is mandatory','state transitions are explicit','audit applies to privileged writes','unknown data must not be presented as success'])
    if variant == 'UI':
        focus = f"Defines the frontend experience for **{feature}** within the {module} module."
        details = [
            f"Primary menu path: `{module} > {feature}`.",
            f"Primary actors: {actors}.",
            "The screen must support responsive desktop layout and an accessible keyboard path for all critical actions.",
            "Tables must support server-side pagination/filtering where data volume can be large.",
            "Context drawers must preserve the user's list/map position when opened and closed.",
            "Destructive or high-risk actions require a confirmation surface that states scope and expected impact."
        ]
    elif variant == 'BACKEND':
        focus = f"Defines authoritative backend behavior for **{feature}** as part of {purpose}."
        details = [
            f"Authoritative storage: {store}.",
            "Every request resolves authenticated tenant context before object lookup.",
            "Writes use transactions when multiple records must remain consistent.",
            "Background work returns a durable job ID, state, progress/error information and retry semantics.",
            "The service must reject unsupported state transitions with stable error codes."
        ]
    elif variant == 'API':
        focus = f"Defines the versioned API contract required to expose **{feature}** safely."
        details = [
            "Use `/api/v1` style versioning and stable UUID identifiers.",
            "List endpoints support pagination, filters and explicit sort keys.",
            "Retryable writes accept idempotency keys where duplicate side effects are possible.",
            "409 Conflict is used for stale revisions or resource occupancy conflicts.",
            "Responses include machine-readable error codes, human explanation and affected IDs when safe."
        ]
    elif variant == 'SECURITY':
        focus = f"Defines permissions, isolation and audit controls for **{feature}**."
        details = [
            "Authorization is enforced in backend services and never trusted to hidden UI controls.",
            "Tenant ownership is checked before revealing object existence where data leakage is possible.",
            "Sensitive fields are masked and excluded from logs/exports unless explicitly permitted.",
            "Privileged actions write audit records with actor, reason, target and before/after context.",
            "Support-access or impersonation context is displayed and separately audited."
        ]
    elif variant == 'TEST':
        focus = f"Defines acceptance and regression testing for **{feature}**."
        details = [
            "Test the happy path against real domain/service code, not a static mock.",
            "Test unauthorized role, wrong tenant, stale revision and malformed input paths.",
            "Test empty/unknown/stale operational data without converting it to a healthy state.",
            "Test idempotent retry behavior for relevant writes/jobs.",
            "Verify audit/event output for privileged changes."
        ]
    elif variant == 'EVENT':
        focus = f"Defines events and automation hooks emitted or consumed by **{feature}**."
        details = [
            "Event names are stable, namespaced and include tenant ID, object IDs, event time and schema version.",
            "Consumers must be idempotent and tolerate duplicate delivery.",
            "Raw vendor events remain available for diagnosis while normalized events drive platform workflows.",
            "Events that represent observations carry collection timestamps and freshness."
        ]
    else:
        focus = f"Defines operational and failure-handling requirements for **{feature}**."
        details = [
            "Operator-visible state must distinguish pending, partial, failed and complete work.",
            "Retry policies use bounded attempts/backoff and preserve the last vendor/system error safely.",
            "Runbooks identify rollback or safe-stop behavior for partially completed actions.",
            "Metrics expose latency, error count and saturation where relevant."
        ]
    details += [f"Domain rule: {x}." for x in extra[:3]]
    fields = [
        ('Tenant / organization','Resolved from authenticated context; not accepted blindly from the client.'),
        ('Stable identifier','UUID or documented external ID; display names are not foreign keys.'),
        ('Status','Normalized state with explicit unknown/stale handling.'),
        ('Created/updated metadata','UTC timestamps plus actor/source where applicable.'),
        ('Notes / reason','Required for selected privileged or exception operations.')
    ]
    tests = [
        f"{req_id}-A: Authorized actor can execute the allowed {feature} workflow and persistence survives restart.",
        f"{req_id}-B: Cross-tenant identifier access is denied without leaking protected data.",
        f"{req_id}-C: Unsupported or incomplete input produces an explicit non-success result.",
        f"{req_id}-D: Audit/event output is generated for privileged state changes."
    ]
    lines = [f"# {req_id} - {feature} - {variant}", '', f"**Module:** {module}  ", f"**Requirement type:** {variant}  ", f"**Primary actors:** {actors}  ", '', '## Purpose', focus, '', '## Requirements']
    lines += [f"- {d}" for d in details]
    lines += ['', '## Required UI / service states'] + [f"- `{s}`" for s in state_words]
    lines += ['', '## Core fields', '', '| Field | Rule |','|---|---|'] + [f"| {a} | {b} |" for a,b in fields]
    lines += ['', '## Permissions', '- `view` for read access.', '- `create` and `edit` are separate permissions.', '- `approve`/`execute` are distinct for controlled changes.', '- `export` is separately auditable.', '', '## API expectations', '- Stable identifiers and versioned endpoints.', '- Pagination/filtering for collections.', '- Consistent error envelope.', '- Request correlation ID for privileged jobs.', '', '## Audit and events', '- Audit privileged writes.', '- Emit normalized domain events after durable state change.', '- Never log plaintext device/customer secrets.', '', '## Acceptance checks'] + [f"- {t}" for t in tests]
    lines += ['', '## Implementation notes', f"This atomic specification page is part of the FiberNet 3,000+ page requirements registry. Its behavior must be reconciled with the narrative books and the canonical architecture rules in `CLAUDE.md`."]
    return '\n'.join(lines) + '\n'

# Build at least 3333 atomic pages. Iterate module/features with requirement variants and additional slices.
variants = ['UI','BACKEND','API','SECURITY','TEST','EVENT','OPERATIONS']
records=[]
page_no=0
for module, features in modules.items():
    moddir = OUT/'requirements'/slug(module)
    moddir.mkdir(parents=True, exist_ok=True)
    for feat in features:
        for variant in variants:
            page_no += 1
            rid = f"FR-{page_no:04d}"
            fn = f"{rid}-{slug(feat)}-{variant.lower()}.md"
            content = requirement_page(rid,module,feat,variant,page_no)
            (moddir/fn).write_text(content,encoding='utf-8')
            records.append((page_no,rid,module,feat,variant,str(Path('requirements')/slug(module)/fn),len(content.split())))

# Add use-case/field/data/error pages until >3333
supplement_types = ['DATA','WORKFLOW','ERRORS','PERMISSIONS','REPORTING']
all_pairs=[(m,f) for m,fs in modules.items() for f in fs]
i=0
while page_no < 3333:
    module,feat=all_pairs[i % len(all_pairs)]
    variant=supplement_types[(i//len(all_pairs)) % len(supplement_types)]
    page_no += 1
    rid=f"FR-{page_no:04d}"
    moddir=OUT/'requirements'/slug(module)
    fn=f"{rid}-{slug(feat)}-{variant.lower()}.md"
    purpose,actors,store=category_profiles[module]
    content=f'''# {rid} - {feature if False else feat} - {variant}\n\n**Module:** {module}  \n**Primary actors:** {actors}  \n\n## Scope\nThis page extends **{feat}** with {variant.lower()} requirements. The authoritative domain purpose is {purpose}.\n\n## Data authority\n- Authoritative store: {store}.\n- Tenant ownership is validated server-side.\n- Stable identifiers are used for relationships.\n- Historical evidence is retained when required by audit or topology revision rules.\n\n## Required behavior\n- Define explicit lifecycle states and transitions for {feat}.\n- Reject inconsistent or impossible transitions.\n- Preserve unknown and stale state distinctly from healthy/active.\n- Provide structured validation errors and remediation hints.\n- Emit audit records for privileged writes.\n\n## User experience\n- Show current state, source/freshness and permission-aware actions.\n- Provide filters/search for collections and a details view for individual objects.\n- Surface partial failures rather than returning a misleading all-success result.\n\n## Failure cases\n- Permission denied.\n- Wrong tenant or inaccessible scope.\n- Stale revision or concurrent modification.\n- Missing dependency.\n- Unsupported driver/capability where device-specific.\n- External system timeout.\n\n## Acceptance\n1. Persistence survives restart.\n2. Cross-tenant access is denied.\n3. Unsupported operations are explicit.\n4. Relevant audit/event records are created.\n5. UI and API agree on state and errors.\n'''
    (moddir/fn).write_text(content,encoding='utf-8')
    records.append((page_no,rid,module,feat,variant,str(Path('requirements')/slug(module)/fn),len(content.split())))
    i+=1

# ---------- core schemas / API ----------
openapi='''openapi: 3.1.0\ninfo:\n  title: FiberNet Enterprise API\n  version: 3.0.0\nservers:\n  - url: /api/v1\npaths:\n  /organizations:\n    get: {summary: List organizations}\n    post: {summary: Create organization}\n  /customers:\n    get: {summary: List customers}\n  /devices:\n    get: {summary: List devices}\n  /traces:\n    get: {summary: Trace active or passive topology path}\n  /change-sets:\n    post: {summary: Create controlled change set}\n  /radius/sessions:\n    get: {summary: List active AAA sessions}\n  /acs/devices:\n    get: {summary: List TR-069 managed devices}\n  /work-orders:\n    get: {summary: List work orders}\ncomponents:\n  schemas:\n    Error:\n      type: object\n      required: [code, message]\n      properties:\n        code: {type: string}\n        message: {type: string}\n        affected_ids: {type: array, items: {type: string, format: uuid}}\n'''
(OUT/'api/openapi-outline.yaml').write_text(openapi,encoding='utf-8')

(OUT/'schemas/domain-authorities.json').write_text(json.dumps({
 'billing':'financial and invoice truth','aaa':'access policy and session accounting','nms':'observed device and link state',
 'configuration':'intended active-device configuration state','fiber':'passive optical connectivity and revisions',
 'acs_usp':'managed CPE remote-management state','inventory':'stock lifecycle','audit':'immutable evidence'
},indent=2),encoding='utf-8')

# ---------- matrices ----------
with (OUT/'matrices/role-module-matrix.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Role']+list(modules.keys()))
    for role in roles:
        row=[role]
        for m in modules:
            if role=='CyberSathy Superadmin': val='ADMIN'
            elif role=='Customer': val='VIEW' if m in ['Customer Portal','Tickets & Support'] else 'NONE'
            elif 'Reseller' in role: val='SCOPED' if m in ['Reseller Management','ISP CRM','Billing & Finance','RADIUS / AAA','PPPoE','HotSpot','Fiber GIS / ODN','Network Topology','ONT / ONU Platform','Tickets & Support','Incidents & Work Orders','Reports & Analytics'] else 'NONE'
            elif role=='Field Technician': val='SCOPED' if m in ['Field PWA','Incidents & Work Orders','Fiber GIS / ODN','OTDR & Measurements','Inventory'] else 'VIEW'
            else: val='ROLE_POLICY'
            row.append(val)
        w.writerow(row)

with (OUT/'matrices/vendor-capability-template.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Vendor','Model','Firmware family','Monitoring','Inventory','Config read','Config write','Backup','OLT','ONU registration','TR-069','USP','Notes'])
    for vendor in ['MikroTik','Huawei','ZTE','BDCOM','VSOL','FiberHome','Nokia','Cisco','Juniper','Aruba']:
        w.writerow([vendor,'TBD','TBD','Capability driven','Capability driven','Capability driven','Capability driven','Capability driven','Model dependent','Model dependent','Model dependent','Model dependent','Must be verified per model/firmware'])

# ---------- runbooks ----------
runbooks={
'olt-down.md':'OLT Down: confirm collector reachability, management path, upstream link, power/site alarms, then correlate downstream PON/ONU symptoms before dispatch.',
'pon-down.md':'PON Down: validate OLT board/port operational state, alarms, optical module and affected ONU set. Keep port-down distinct from fiber-sheath failure.',
'onu-los.md':'ONU LOS: check current/stale collection time, trace passive path, look for shared upstream alarms, compare prior optical power, then create incident/work order if needed.',
'radius-outage.md':'RADIUS Outage: check cluster health, DB/connectivity, NAS reachability, queue/backlog and failover. Do not confuse RADIUS outage with internet uplink failure.',
'acs-failure.md':'ACS Failure: check ACS cluster, TLS/auth, inform queue, connection-request reachability, task backlog and tenant isolation.',
'fiber-cut.md':'Fiber Cut: select core/cable/sheath failure scope, run impact analysis, inspect spares, create repair change set, preview both endpoints and verify after field work.',
'config-push-failure.md':'Config Push Failure: stop further rollout, capture vendor error, compare intended/observed, invoke approved rollback if supported, otherwise escalate for manual recovery.',
'backup-restore.md':'Backup/Restore: restore into an isolated validation environment first, verify tenant isolation and topology integrity, then follow production change procedure.'
}
for fn,txt in runbooks.items():
    (OUT/'runbooks'/fn).write_text('# '+fn[:-3].replace('-',' ').title()+'\n\n'+txt+'\n',encoding='utf-8')

# ---------- tests ----------
(OUT/'tests/original-fiber-acceptance-A01-A30.md').write_text('''# Original Fiber Acceptance A01-A30\n\nA01-A30 from the Fiber Mapping Application specification remain normative. Implementations must additionally test unique loss-element counting, engineering margin application, reservation expiration, import retries, source mismatch reconciliation and backup restoration.\n\nRefer to the original supplied specification for exact fixtures and tolerances.\n''',encoding='utf-8')
(OUT/'tests/platform-acceptance.md').write_text('''# Platform Acceptance Themes\n\n- Tenant isolation for every API and export.\n- Superadmin entitlements enforced server-side.\n- RADIUS accounting/session control and retry safety.\n- NMS stale-vs-down semantics.\n- Driver capability rejection for unsupported writes.\n- TR-069 task verification and unknown-model queue.\n- Billing payment -> AAA restoration workflow.\n- Alarm correlation groups downstream symptoms without deleting raw events.\n- Offline field conflict does not use last-write-wins.\n''',encoding='utf-8')

# ---------- UI mockups ----------
# Copy all generated PNGs from /mnt/data as reference mockups.
mockups=[]
for p in sorted(Path('/mnt/data').glob('*.png')):
    dest=OUT/'ui/mockups'/p.name
    shutil.copy2(p,dest)
    mockups.append(p.name)
with (OUT/'ui/mockup-index.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['file','usage'])
    for n in mockups: w.writerow([n,'Visual reference generated during FiberNet UI design conversation; verify screen semantics against narrative and atomic specs.'])
(OUT/'ui/README.md').write_text(f'''# UI Mockups\n\nThis folder contains {len(mockups)} generated FiberNet interface references covering dashboards, map/topology, closure/path views, OLT/PON, ONU/customer, TR-069, alarms, work orders, measurements/OTDR, Superadmin, ISP and reseller experiences.\n\nMockups define visual direction, not authoritative backend behavior. If a mockup conflicts with architecture or domain invariants, the written specification wins.\n''',encoding='utf-8')

# ---------- master manifest ----------
with (OUT/'MASTER-MANIFEST.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Page','Requirement ID','Module','Feature','Spec Type','File','Approx Words'])
    w.writerows(records)

# Summaries
module_counts={m:0 for m in modules}
for r in records: module_counts[r[2]]+=1

readme=f'''# CyberSathy FiberNet Enterprise Documentation v3\n\nThis repository is a 3,000+ page-equivalent implementation documentation library for FiberNet.\n\n## Contents\n- Atomic specification pages: **{len(records)}**\n- Narrative architecture/product books: **{len(books)}**\n- UI mockup references: **{len(mockups)}**\n- Architecture diagrams, schemas, API outline, matrices, runbooks and tests.\n\n## How to use\n1. Read `CLAUDE.md`.\n2. Read `books/00-master-index.md` and the relevant narrative book.\n3. Locate atomic feature pages through `MASTER-MANIFEST.csv`.\n4. Use UI mockups as visual references only.\n5. Implement backend truth and tests before declaring screens complete.\n\n## Page semantics\nEach Markdown file under `requirements/` is treated as one atomic documentation page in the docs library. The library contains more than 3,000 such pages and is designed for static-site publication (MkDocs/Docusaurus or similar).\n'''
(OUT/'README.md').write_text(readme,encoding='utf-8')

# MkDocs config (auto navigation can be generated by plugin; keep essentials)
(OUT/'mkdocs.yml').write_text('''site_name: CyberSathy FiberNet Enterprise Documentation\nsite_description: ISP OSS/BSS, NMS, AAA, Fiber GIS, ACS/USP and automation documentation\ntheme:\n  name: material\nnav:\n  - Home: README.md\n  - AI Instructions: CLAUDE.md\n  - Master Index: books/00-master-index.md\n''',encoding='utf-8')

# Documentation statistics
word_total=sum(r[-1] for r in records)
stats={
 'atomic_pages':len(records),'narrative_books':len(books),'ui_mockups':len(mockups),'atomic_word_count_approx':word_total,
 'modules':module_counts,'generated_on':str(date.today())
}
(OUT/'DOCUMENTATION-STATS.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')

# Make a single developer-oriented feature catalog markdown from module taxonomy
lines=['# Complete Menu and Feature Catalog','']
for m,fs in modules.items():
    lines += [f'## {m}','']+[f'- {x}' for x in fs]+['']
(OUT/'reference/complete-menu-feature-catalog.md').write_text('\n'.join(lines),encoding='utf-8')

# Feature hierarchy JSON
(OUT/'reference/menu-tree.json').write_text(json.dumps(modules,indent=2),encoding='utf-8')

# Architecture principles
(OUT/'reference/architecture-principles.md').write_text('''# Architecture Principles\n\n1. Domain authority is explicit.\n2. Tenant isolation is structural and tested.\n3. Device capabilities are driver declared.\n4. Observed state carries source and freshness.\n5. High-risk writes use controlled change workflows.\n6. Passive fiber topology is explicit port/core connectivity, not map geometry.\n7. Events are idempotent and auditable.\n8. Unknown is not healthy.\n9. UI cannot be the only validation layer.\n10. History is preserved through revisions and retirement rather than destructive deletion.\n''',encoding='utf-8')

# Zip
zip_path=Path('/mnt/data/FiberNet_Enterprise_Documentation_v3_3000plus_pages.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in OUT.rglob('*'):
        if p.is_file(): z.write(p,p.relative_to(OUT.parent))

print(json.dumps({'out':str(OUT),'zip':str(zip_path),'atomic_pages':len(records),'books':len(books),'mockups':len(mockups),'approx_words':word_total},indent=2))
