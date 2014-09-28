# -*- coding: utf-8 -*-
import sys, ConfigParser
path="/root/admin/switch/arista/python-rpc"
if path not in sys.path:
    sys.path.append(path)
    
import sys
from arista_rpc import SwitchConnection, Vlan, SwitchConfig, Interface
from utils import Console, StringUtil

# 실행 테스트 필요
# forbiz server를 Ethernet21에 붙었다고 가정하고 테스트
# Ethernet21이 유휴 포트인지 체크
"""
vUTM 시범서비스 도입 시에 현재 구성된 고객 서버의 GW IP 변경이 필요함
현재는 고객 서버의 GW IP가 192.168.0.1 이고, 이 GW가 VLAN 11에서는 접근 가능함
따라서 고객 서버의 VLAN을 현재의 10번에서 11로 변경해주어 
VLAN 11에 있는 GW를 통해 고객사 담당자가 고객 서버에 접근해 
서버의 GW IP를 새로운 GW인 192.168.0.254로 수정할 수 있도록 해주고,
그 후 다시 서버의 VLAN을 10으로 변경해주어 서버가 새로운 GW로 외부와 연결될 수 있도록 해준다. 
"""
"""
이 프로그램은 고객사 서버 목록에 있는 모든 서버를 
    1. 임시 VLAN으로 이전하거나, 
    2. 다시 원래의 VLAN으로 이전
한다.  
 
*** switch.cfg설정 파일에서 
[forbiz] 탭의 server 키값은 고객사의 서버 목록을 제공한다.
server=forbiz-server

*** 각 서버의 네트워크 구성에 대한 정보는 서버 명으로 접근 가능하다. 

# 고객사 서버중 Orange망 설정
[forbiz-server]
nic=eth2
port=Ethernet20
port_mode=access
port_vlan=forbiz:orange

*** [migration] 탭에는 임시로 이동할 vlan 값을 설정한다. 

[migration]
temp_vlan=forbiz:green

*** forbiz:green의 VLAN ID는 [forbiz] 탭에서 확인할 수 있다

# 고객사에서 이용하는 VLAN 정보 - 포비즈
[forbiz]
green=11
orange=10
server=forbiz-server

"""
def usage(argv):
    print "Usage: %s [customer] [origin or temp]" % argv[0]
    print "   - to use original vlan: %s forbiz origin" % argv[0]
    print "   - to use temporal vlan: %s forbiz temp" % argv[0]
    sys.exit()    

# 설정
# configuration parsing 하는 부분을 따로 만들어야 할 듯....
def apply_configuration(cfg, tmp_vlan_id, argv):
    list_server = (cfg.get(customer, "servers")).split(",")
    for server in list_server:
        server = server.strip()
        
        port = cfg.get(server, "port")
        intf = Interface(port)
        
        cfg_vlan = cfg.get(server, "port_vlan").split(":")
        cfg_vlan_id = cfg.get(cfg_vlan[0], cfg_vlan[1])
        
        if target == "origin":
            intf.set_access_vlan(cfg_vlan_id)
        elif target == "temp":
            intf.set_access_vlan(tmp_vlan_id)
        else:
            usage(argv)                

# 설정내용 확인
def check_configuration(cfg, tmp_vlan_id, argv):
    list_server = (cfg.get(customer, "servers")).split(",")
    for server in list_server:
        server = server.strip()
        
        port = cfg.get(server, "port")
        intf = Interface(port)
        
        cfg_vlan = cfg.get(server, "port_vlan").split(":")
        cfg_vlan_id = cfg.get(cfg_vlan[0], cfg_vlan[1])
        
        current_vlan_id = intf.get_vlan()
        if target == "origin":
            if current_vlan_id.strip() == cfg_vlan_id.stip():
                Console().info("*** Configuration has been successfully applied!!!")
            else:
                Console().error("*** Failed to apply configuration!!!")
            Console().log("    %s interface= %s" % (server, port))
            Console().log("       vlan_origin= %s" % cfg_vlan_id)
            Console().log("       vlan_current= %s" % current_vlan_id)
        elif target == "temp":
            if current_vlan_id.strip() == tmp_vlan_id.stip():
                Console().info("*** Configuration has been successfully applied!!!")
            else:
                Console().error("*** Failed to apply configuration!!!")
            Console().log("    %s interface= %s" % (server, port))
            Console().log("       vlan_temp= %s" % tmp_vlan_id)
            Console().log("       vlan_current= %s" % current_vlan_id)
        else:
            usage(argv)          

def main():
    if len(sys.argv) < 3: 
        usage(sys.argv)
    
    cfg = SwitchConfig().get_config()
    
    customer = sys.argv[1]
    target = sys.argv[2] 
    
    cfg_tmp_vlan = cfg.get("migration", "tmp_vlan").split(":")
    tmp_vlan_id = cfg.get(cfg_tmp_vlan[0], cfg_tmp_vlan[1])
    
    apply_configuration(cfg, tmp_vlan_id, argv)
    check_configuration(cfg, tmp_vlan_id, argv)
       
        
if __name__ == "__main__":
    main()

