#!/usr/bin/python

from arista import SwitchConnection, VLAN, Interface, MgmtInterface, Routing

mgmtIp="211.224.204.148"
mgmtUser="admin"
mgmtPass="ohhberry3333"

def main():
    switch = SwitchConnection(mgmtIp, mgmtUser, mgmtPass)
    conn = switch.connect()

    eth_list = []

    eth = Interface(13, conn)
    eth._access_vlan("Mgmt-Network", 4)
    eth_list.append(eth)

    eth = Interface(45, conn)
    eth.set_trunk("2001-4000")
    eth_list.append(eth)

    eth = Interface(46, conn)
    eth.set_trunk("10-2000")
    eth_list.append(eth)

    for eth in eth_list:
        eth.show_running_config()

    conn.close()
 
if __name__ == "__main__":
    main()
