# OLT and ONT Provisioning

OLT provisioning is model and firmware aware. Device definitions include chassis, boards, PON technologies, authentication methods, line profiles, service profiles, DBA, T-CONT, GEM, VLAN, service-port and OMCI capabilities.

ONU registration workflow: discover -> classify model -> validate serial/LOID -> allocate ONU ID -> select profiles -> register -> configure management/service paths -> configure TR-069/USP where applicable -> read back -> optical validation -> customer association -> audit.

The platform must distinguish documented configuration from observed OLT state and surface mismatches.
