# -*- coding: utf-8 -*-
import sys, ConfigParser
path="/root/admin/switch/arista/python-rpc"
if path not in sys.path:
    sys.path.append(path)
    
import sys
from arista_rpc import SwitchConnection, Vlan, SwitchConfig, Interface
from utils import Console, StringUtil

"""
UTM VM 다운이나 Cloud C-node 다운 시에 Baremetal UTM으로 절체해주는 기능
원래는 Trunk port에서 UTM용 GREEN이나 ORANGE VLAN을 제거해주는 형태로 동작해야 하나, 여기에서는 스위치의 포트를 shutdown시키는 형태로만 동작
"""

def usage(argv):
    print "Usage: %s [baremetal or baremetal]" % argv[0]
    print "   - to use baremetal: %s baremetal" % argv[0]
    print "   - to use cloud    : %s cloud" % argv[0]
    sys.exit()    

def revert(cfg, cloud, barem):
    intf_cloud = Interface(cloud)
    intf_barem = Interface(barem)
    
    Console().log("Shutdown Bare-metal interface= %s" % intf_cloud.interface_id)
    intf_cloud.shutdown(False)

    print "bare-metal interface status= %s" % intf_barem.get_status()
    
    Console().log("Enable Cloud C-node interface= %s" % intf_barem.interface_id)
    intf_barem.shutdown(True)  
    print "c-node interface status= %s" % intf_cloud.get_status()
    
def failover(cfg, cloud, barem):
    intf_cloud = Interface(cloud)
    intf_barem = Interface(barem)
    
    Console().log("Shutdown Cloud C-node interface= %s" % intf_cloud.interface_id)
    intf_cloud.shutdown(True)
    print "c-node interface status= %s" % intf_cloud.get_status()
    
    Console().log("Enable Bare-metal interface= %s" % intf_barem.interface_id)
    intf_barem.shutdown(False)  
    print "bare-metal interface status= %s" % intf_barem.get_status()
  
def main():
    if len(sys.argv) < 2: 
        usage(sys.argv)
    
    cfg = SwitchConfig().get_config()
    
    fo_cloud = cfg.get("failover", "cloud")
    fo_barem = cfg.get("failover", "baremetal")
    
    port_cloud = cfg.get(fo_cloud, "port_hybrid")
    port_barem = cfg.get(fo_barem, "port_green")
    
    target = sys.argv[1]    

    if target == "baremetal":
        failover(cfg, port_cloud, port_barem)
    elif target == "cloud":
        revert(cfg, port_cloud, port_barem)
    else:
        usage(argv)
    
if __name__ == "__main__":
    main()

