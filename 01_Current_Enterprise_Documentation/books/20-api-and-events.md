# API and Event Architecture

All external APIs are versioned, authenticated and tenant scoped. Write operations support idempotency where retries are expected. 409 is used for stale revision or occupancy conflicts. Validation errors return stable codes, affected IDs and remediation hints.

Domain events use stable names such as device.down, interface.down, onu.los, payment.received, radius.login, workorder.completed and topology.commissioned. Consumers must be idempotent.
