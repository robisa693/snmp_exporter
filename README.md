# snmp_exporter
Does an snmpget on specified devices and converts into prometheus metrics hosted on localhost:8000. 
Ready for the taking, I mean scraping.

## edit config.ini
A bit messy but just add more entries in the config.ini file as instructed inside.
TODO: Segment to configuration file into more readable form.

## Output of a curl requst
Each entry in the config file will be its own metric
```bash
$ curl localhost:8000
# HELP fw_cpu_total_util total cpu utilization of junos fw
# TYPE fw_cpu_total_util gauge
fw_cpu_total_util{instance="fwhostname1"} 5.0
# HELP fw_cpu_total_util total cpu utilization of junos fw
# TYPE fw_cpu_total_util gauge
fw_cpu_total_util{instance="fwhostname2"} 4.0
```
