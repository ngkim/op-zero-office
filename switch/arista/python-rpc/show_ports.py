# -*- coding: utf-8 -*-
from arista_rpc import SwitchConnection, Vlan, SwitchConfig

"""
arista_rpc를 이용하여 vlan에 구성된 인터페이스 목록을 보여준다.

root@manager:~/admin/switch/arista/python-rpc# python show_ports.py 
=== Access Ports ===
* vlan= Mgmt-Network             id= 4    
    - Ethernet1
    - Ethernet2
    - Ethernet3
    - Ethernet4

* vlan= API-Network              id= 3    
    - Ethernet11
    - Ethernet12
    - Ethernet13

* vlan= External-Network(221)    id= 2000 
    - Ethernet23
    - Ethernet24

* vlan= Forbiz-Green             id= 11   
    - Ethernet19
    - Ethernet21

* vlan= Forbiz-Orange            id= 10   
    - Ethernet20

* vlan= Test-Green               id= 21   

* vlan= Test-Orange              id= 20   

=== Trunk Ports ===
* vlan= OpenStack-Private        id= 2001 
    - Ethernet45
    - Ethernet47
    - Ethernet6

* vlan= "Forbiz-Orange"          id= 10   
    - Ethernet10
    - Ethernet46
    - Ethernet48
    - Ethernet9

"""
def show_access_ports(vlanList):
    for vlan in vlanList:
        vlan.show_access_ports()

def show_trunk_ports(vlanList):
    for vlan in vlanList:
        vlan.show_trunk_ports()

def get_vlan_ports():
    proxy = SwitchConnection().get_proxy()
    cfg = SwitchConfig().get_config()
    
    # Management VLAN, API VLAN, External VLAN
    mgmtVlanId = cfg.get("access_vlan", "mgmt_vlan")
    apiVlanId = cfg.get("access_vlan", "api_vlan")
    extVlanId = cfg.get("access_vlan", "ext_vlan")
    
    privateVlanId = cfg.get("private", "min")
    hybridVlanId = cfg.get("hybrid", "min")
    
    forbizGreen = cfg.get("forbiz", "green")
    forbizOrange = cfg.get("forbiz", "orange")
    
    testGreen = cfg.get("test", "green")
    testOrange = cfg.get("test", "orange")
    
    mgmtVlan = Vlan(mgmtVlanId)
    apiVlan = Vlan(apiVlanId)
    extVlan = Vlan(extVlanId, "External-Network(221)")
    
    privateVlan = Vlan(privateVlanId, "OpenStack-Private")
    hybridVlan = Vlan(hybridVlanId)
    
    forbizGreenVlan = Vlan(forbizGreen, "Forbiz-Green")
    forbizOrangeVlan = Vlan(forbizOrange, "Forbiz-Orange")
    
    testGreenVlan = Vlan(testGreen, "Test-Green")
    testOrangeVlan = Vlan(testOrange, "Test-Orange")
    
    accessVlanList = [mgmtVlan, apiVlan, extVlan, forbizGreenVlan, forbizOrangeVlan, testGreenVlan, testOrangeVlan]
    trunkVlanList = [privateVlan, hybridVlan]
    
    print "=== Access Ports ==="
    show_access_ports(accessVlanList)
    print "=== Trunk Ports ==="
    show_trunk_ports(trunkVlanList)    
 
if __name__ == "__main__":
    get_vlan_ports()
    