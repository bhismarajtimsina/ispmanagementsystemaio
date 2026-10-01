# NMS Architecture

NMS uses distributed collectors near managed networks. Collectors perform SNMPv3, ICMP, syslog/trap ingestion, REST/NETCONF/SSH/vendor API calls and supported streaming telemetry. They publish normalized inventory, metrics and events to the central platform over authenticated encrypted channels.

Metrics belong in a time-series store; business/topology metadata belongs in PostgreSQL/PostGIS. Redis supports caching and jobs. Device credentials are references into a secret store.

Observed topology is derived from LLDP/CDP, MAC/ARP tables and routing adjacencies, then reconciled against documented topology. Discovery never overwrites human-maintained authoritative links without review.
