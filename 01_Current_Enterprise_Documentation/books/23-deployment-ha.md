# Deployment, High Availability and Disaster Recovery

Production separates web/API nodes, background workers, collectors, RADIUS, ACS/USP services, PostgreSQL, Redis, time-series storage and object storage. Health, backups and restoration are tested. Critical services support horizontal scaling where appropriate.

Collectors buffer telemetry during WAN interruption and resume with timestamps rather than pretending the devices were down.
