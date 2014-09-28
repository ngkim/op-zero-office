#!/usr/bin/python

from arista import SwitchConnection, VLAN, Interface, MgmtInterface, Routing

mgmtIp="211.224.204.148"
mgmtUser="admin"
mgmtPass="ohhberry3333"

def main():
    switch = SwitchConnection(mgmtIp, mgmtUser, mgmtPass)
    conn = switch.connect()

    trunk_range = "10-2000"

    eth17 = Interface(17, conn)

    eth17.show_running_config()

    eth17.set_trunk(trunk_range)

    eth17.show_running_config()

    conn.close()
 
if __name__ == "__main__":
    main()
