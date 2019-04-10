from pyroute2 import IPDB # pip3 install pyroute2
from netaddr import * # pip3 install netaddr

def getTunGW():
    ip = IPDB()
    ifdb = ip.interfaces
    #Loops until the ipv4 address is learned. Then gets it.
    if len(ifdb.tun0.ipaddr.ipv4) == 0:
        return None
    tunAddr = ifdb.tun0.ipaddr.ipv4[0]

    tunIp = tunAddr['address']
    tunMask = tunAddr['prefixlen']

    #gets the network object representing the VPN
    tunNet = IPNetwork(str(tunIp)+'/'+str(tunMask))

    #Obtains the first IP of the subnet. With Openvpn, the server always has the first IP.
    tunGW = tunNet[1]
    return tunGW

