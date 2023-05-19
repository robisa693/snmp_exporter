from prometheus_client import start_http_server
from prometheus_client import Gauge, Histogram, Summary
from prometheus_client.core import GaugeMetricFamily, CollectorRegistry
import requests
import socket
import configparser
import os
import sys
import time

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




if __name__ == '__main__':

    ### test of configparser ###
    c = ConfigParser()
    ### test of configparser ###
    registry = CollectorRegistry()
    registry.register(SNMPCollector)
    start_http_server(8000, registry=registry)
    while True:
        time.sleep(1)