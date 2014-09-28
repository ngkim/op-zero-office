# -*- coding: utf-8 -*-
import sys, ConfigParser
path="/root/admin/switch/arista/python-rpc"
if path not in sys.path:
    sys.path.append(path)
    
import sys
from arista_rpc import SwitchConnection, Vlan, SwitchConfig, Interface
from utils import Console, StringUtil

"""
failover한 interface의 status를 체크
"""

def check_status(cfg, cloud, barem):
    intf_cloud = Interface(cloud)
    intf_barem = Interface(barem)
    
    print "c-node interface= %s status= %s" % (cloud, intf_cloud.get_status())
    print "bare-metal interface= %s status= %s" % (barem, intf_barem.get_status())

def main():
    cfg = SwitchConfig().get_config()
    
    fo_cloud = cfg.get("failover", "cloud")
    fo_barem = cfg.get("failover", "baremetal")
    
    port_cloud = cfg.get(fo_cloud, "port_hybrid")
    port_barem = cfg.get(fo_barem, "port_green")
    
    check_status(cfg, port_cloud, port_barem)
    
if __name__ == "__main__":
    main()

