#!/usr/bin/python

from arista import SwitchConnection, VLAN, Interface, MgmtInterface, Routing

mgmtIp="211.224.204.148"
mgmtUser="admin"
mgmtPass="ohhberry3333"
vlanId="38"

def main():
    switch = SwitchConnection(mgmtIp)
    conn = switch.connect(mgmtUser, mgmtPass)

    vlanId = 4
    vlan_mgmt = VLAN("Mgmt-Network", vlanId, conn) 
    vlan_mgmt.create_if_not_exist()
   
    eth1 = Interface(1, conn)
    eth1.set_speed()
    eth2 = Interface(2, conn)
    eth3 = Interface(3, conn)
    eth4 = Interface(4, conn)

    eth1.access_vlan(vlan_mgmt)
    eth2.access_vlan(vlan_mgmt)
    eth3.access_vlan(vlan_mgmt)
    eth4.access_vlan(vlan_mgmt)

    trunk_range = "2001-4000"

    eth5 = Interface(5, conn)
    eth5.set_trunk(trunk_range)

    eth6 = Interface(6, conn)
    eth6.set_trunk(trunk_range)

    eth7 = Interface(7, conn)
    eth7.set_trunk(trunk_range)

    eth8 = Interface(8, conn)
    eth8.set_trunk(trunk_range)

    eth47 = Interface(47, conn)
    eth47.set_trunk(trunk_range)

    trunk_range = "10-2000"

    eth9 = Interface(9, conn)
    eth9.set_speed()
    eth9.set_trunk(trunk_range)

    eth10 = Interface(10, conn)
    eth10.set_trunk(trunk_range)

    eth48 = Interface(48, conn)
    eth48.set_trunk(trunk_range)

    vlanId = 3
    vlan_api_ = VLAN("API-Network", vlanId, conn) 
    vlan_api.create_if_not_exist()

    eth11 = Interface(11, conn)
    eth12 = Interface(12, conn)
    eth12.set_speed()
    eth13 = Interface(13, conn)
    eth14 = Interface(14, conn)
    eth15 = Interface(15, conn)
    eth16 = Interface(16, conn)

    eth11.access_vlan(vlan_api)
    eth12.access_vlan(vlan_api)
    eth13.access_vlan(vlan_api)
    eth14.access_vlan(vlan_api)
    eth15.access_vlan(vlan_api)
    eth16.access_vlan(vlan_api)

    vlanId = 2000
    vlan_ext_red = VLAN("EXT-Red", vlanId, conn) 
    vlan_ext_red.create_if_not_exist()

    eth18 = Interface(18, conn)
    eth18.set_speed()
    eth18.access_vlan(vlan_ext_red)

    eth22 = Interface(22, conn)
    eth22.set_speed()
    eth22.access_vlan(vlan_ext_red)

    eth24 = Interface(24, conn)
    eth24.set_speed()
    eth24.access_vlan(vlan_ext_red)

    vlanId = 11
    vlan_green = VLAN("Green", vlanId, conn) 
    vlan_green.create_if_not_exist()

    eth19 = Interface(19, conn)
    eth19.access_vlan(vlan_green)

    eth21 = Interface(21, conn)
    eth21.set_speed()
    eth21.access_vlan(vlan_green)

    vlanId = 10
    vlan_orange = VLAN("Orange", vlanId, conn) 
    vlan_orange.create_if_not_exist()

    eth20 = Interface(20, conn)
    eth20.access_vlan(vlan_orange)

    vlanId = 2
    vlan_ext_data = VLAN("External-Data-Network", vlanId, conn) 
    vlan_ext_data.create_if_not_exist()

    mgmt = MgmtInterface()
    mgmt.set_ip_address("221.224.204.148/27")

    routing = Routing()
    routing.enable_routing()
    routing.add_ip_route("0.0.0.0/0", "211.224.204.129")

    conn.close()

def test():
    switch = SwitchConnection(mgmtIp)
    conn = switch.connect(mgmtUser, mgmtPass)

    vlanId = 4
    vlan_mgmt = arista.VLAN("Mgmt-Network", vlanId, conn) 
    vlan_mgmt.create_if_not_exist()

    conn.close()
 
if __name__ == "__main__":
#    main()
     test()
