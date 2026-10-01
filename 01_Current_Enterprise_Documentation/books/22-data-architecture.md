# Data Architecture

PostgreSQL/PostGIS stores tenants, business objects, authoritative topology, revisions and transactional state. A time-series store handles high-cardinality metrics. Redis supports cache and distributed jobs. Object storage keeps photos, documents, config backups, firmware and OTDR files.

Every domain table carries tenant ownership directly or through an enforced parent. Cross-tenant generic foreign keys are prohibited.
