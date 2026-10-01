# Alarms, Events and Incidents

Raw device events are normalized by a global alarm dictionary. Alarm rules add severity, thresholds, deduplication windows, dependencies and notification policies. Correlation can group downstream symptoms under a likely root event, such as suppressing thousands of ONU-offline alarms when an OLT uplink is down.

Incidents remain hypotheses until confirmed. They track scope, services, root cause evidence, assignments, work orders, timeline and RCA.
