from pyroute2 import IPDB # pip3 install pyroute2
from netaddr import * # pip3 install netaddr
from includes.config import *
import socket

def getTunGW():
    """
    Returns a IPAddress object from netaddr lib
    """
    ip = IPDB()
    ifdb = ip.interfaces
    if 'tun0' not in ifdb:
        return None
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

def sendServer(message):
    """
    Sends the string given in parameter to the server
    """
    if config['SRV_IP'] == None:
        ip = str(getTunGW())
    else:
        ip = config['SRV_IP']
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, config['SRV_PORT']))
    message+="\n"
    s.send(message.encode())
    with s.makefile() as sockFile:
        response = sockFile.readline()
    return response.strip()

def getNumber(minimum = None, maximum = None, force=True):
    choix = None
    print("selection d'un nombre entre", minimum, "et",maximum)
    while choix == None:
        strin = input()
        try:
            choix = int(strin)
            if (minimum != None and choix < minimum) or\
              (maximum != None and choix > maximum):
                choix = None
                print("Choix incorrect")
        except ValueError:
            print("Veuillez entrer un nombre")
        if(force == False):
            break
    return choix
