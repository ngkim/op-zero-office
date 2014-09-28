from jsonrpclib import Server

mgmtIp="211.224.204.148"
mgmtUser="admin"
mgmtPass="ohhberry3333"

def main():
    api_url = "http://%s:%s@%s/command-api" % (mgmtUser, mgmtPass, mgmtIp)
    switch = Server(api_url)

    response = switch.runCmds( 1, ["show version"] )
    print "The switch's system MAC addess is", response[0]["systemMacAddress"]

if __name__ == "__main__":
    main()
