#!/usr/bin/python

from arista import SwitchConnection, VLAN, Interface, MgmtInterface, Routing

mgmtIp="211.224.204.148"
mgmtUser="admin"
mgmtPass="ohhberry3333"

def main():
    switch = SwitchConnection(mgmtIp, mgmtUser, mgmtPass)
    conn = switch.connect()

    eth22 = Interface(22, conn)
    eth22.show_running_config()

    eth22.shutdown()

    eth22.show_running_config()

    conn.close()
 
if __name__ == "__main__":
    main()
