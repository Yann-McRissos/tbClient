#!/usr/bin/python3
import os, sys
from includes.config import *
from includes.interfaces import *
FORBIDDEN_INTERFACES = ['eth0', 'vxlan0', 'br0', 'tun0']
if __name__ == "__main__":
    pathname = os.path.dirname(sys.argv[0])
    dirname = os.path.abspath(pathname)
    os.chdir(dirname+"/..")
    username = os.getenv("LOGIN", "")
    password = os.getenv("PASSWORD", "")
    gwInterfaces = getGWInterfaces()
    if len(gwInterfaces) == 0:
        print('{"error":true, "reason":"No default route"}')
        sys.exit(1)
    for interface in gwInterfaces:
        if interface in FORBIDDEN_INTERFACES:
            print('{"error":true, "reason":"'+interface+' has a default route"}')
            sys.exit(1)

    if not tunnelExists():
        #Start openvpn    
        startOVPN("connectScript/client.ovpn", username, password)
        #Wait until the tunnel is up or until the process dies
        #! DOES NOT WAIT AND RETURNS AFTER 120 SECONDS!
        ret = waitForTunnelUp(cli=True)
        if ret == False:
            print('{"error":true, "reason":"Tunnel could not connect", "login":"'+username+'","password":"'+password+'" }')
            killOpenvpn()
            sys.exit(1)

        ret = vxlanExists()
        if ret < 2:
            if ret == 1:
                print('{"error":true, "reason":"Interfaces partially up"}')
                sys.exit(1)
            createInterfaces()
    print('{"error":false}')

