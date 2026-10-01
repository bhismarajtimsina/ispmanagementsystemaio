# Fiber GIS and Passive Optical Topology

PostgreSQL/PostGIS is the source of truth for passive topology. Fiber spans, termination nodes, splices, continuity, component transfer paths, patching and ONU/PON terminations are explicit. Geographic geometry is not connectivity.

The system supports arbitrary core counts, repeated colors across tubes, 10:90/20:80/30:70 couplers, equal splitters, mid-span access, uncut continuity, blue-to-red reroutes, ODFs, adapters and revision history.

Trace states include complete, incomplete, ambiguous, invalid loop, blocked by known damage, incompatible component and unknown optical budget.
