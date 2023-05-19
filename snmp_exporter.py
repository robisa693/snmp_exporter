from prometheus_client import start_http_server
from prometheus_client import Gauge, Histogram, Summary
from prometheus_client.core import GaugeMetricFamily, CollectorRegistry
import requests
import socket
import configparser
import os
import sys
import time
from pysnmp.hlapi import *

class ConfigParser():
##
    def __init__(self) -> None:
        config = self.get_config()
        self.targets = self.get_targets(config)
    
    def get_config(self):
        if not os.path.isfile('config.ini'):
            sys.exit("Could not find config.ini file")
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config
    
    def get_targets(self, config):
        snmp1 = []
        snmp2 = []
        snmp_dict = {}
        for snmp_section in config.sections():
            if snmp_section.startswith('SNMP-'):
                for (k,v) in config.items(snmp_section):
                    snmp_dict[k] = v
                    snmp2.append({snmp_section: snmp_dict['device']})
                #temp_target = snmp_dict.copy()
                #snmp1.append(temp_target)
        print(snmp2)
        return snmp2




class SNMPCollector(object):
    def __init__(self) -> None:
        self.c = ConfigParser()

    def collect(self):
        
        #print("test123") 
        old_metric_name = ''
        for device in self.c.targets:
            success = False
            
            for key in device:
                values = key.split("-") # ['SNMP', 'public', 'OID', '1.3.6.1.4.1.1452.1.2.5.1.3.21.1.4.7', 'fw_cpu_total_util', 'description', 'sekiifw1']
                print(values)
                ip = device[key]
                community = values[1]
                oid = values[3]
                name = values[4]
                description = values[5]
                hostname = values[6]
                print(f'{old_metric_name} + {name}')
                #if old_metric_name != name:
                g_metric = GaugeMetricFamily(name, description, labels=['instance'])
                old_metric_name = name
                for (errorIndication,
                    errorStatus,
                    errorIndex,
                    varBinds) in getCmd(SnmpEngine(),
                                        CommunityData(community),
                                        UdpTransportTarget((ip, 161)),
                                        ContextData(),
                                        ObjectType(ObjectIdentity(oid)),
                                        lookupMib=False,
                                        lexicographicMode=False):
                    if errorIndication:
                        print('test')
                        print(errorIndication, file=sys.stderr)
                        
                    elif errorStatus:
                        print('%s at %s' % (errorStatus.prettyPrint(),
                                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
                        
                    else:
                        for varBind in varBinds:
                            k, v = varBind
                            print('%s = %s' % varBind)
                            success = True
                    if success:
                        g_metric.add_metric(labels=[hostname],value=v)
                    else: 
                        print(f'could not get snmp for: {device}')
                        #comment out this line when not testing
                        g_metric.add_metric(labels=[f'DEBUG_failed_for_{hostname}'],value=0)
            yield g_metric
            #k is the OID
            #v is the value of that OID, can be 5 for exmaple
        
    #    print(varBinds)

if __name__ == '__main__':
    registry = CollectorRegistry()
    registry.register(SNMPCollector())
    start_http_server(8000, registry=registry)
    while True:
       time.sleep(1)