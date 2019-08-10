from pyroute2 import IPDB # pip3 install pyroute2
from netaddr import IPNetwork, IPAddress # pip3 install netaddr
import os, sys, subprocess, time, psutil
from includes.config import *

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

def killOpenvpn():
    try:
        with open(config['PIDFILE'], "r") as pidfile:
            pid = pidfile.read()
    except FileNotFoundError:
        return 

    pid = int(pid.strip())
    try:
        os.kill(pid, psutil.signal.SIGINT)
    except ProcessLookupError:
        return
    os.remove(config['PIDFILE'])

def getGWInterfaces():
    ip = IPDB()
    ifIndices = []
    for route in ip.routes:
        if route.dst == 'default':
            ifIndices.append(route.oif)
    if len(ifIndices) == 0:
        return []
    ifNames = []
    for index in ifIndices:
        ifName = ip.interfaces[index].ifname
        ifNames.append(ifName)
    return ifNames

def tunnelExists():
    """
    True if the tunnel exists.
    False if the tunnel doesn't exist.
    """
    ip = IPDB() 
    ifdb = ip.interfaces
    if 'tun0' in ifdb:
        return True
    return False

def vxlanExists():
    """
    0 if nothing is set up
    1 if vxlan is partially set up
    2 if everything is set ip
    """
    ip = IPDB()
    ifdb = ip.interfaces
    if 'br0' not in ifdb:
        if 'vxlan0' not in ifdb:
            return 0
        return 1
    
    bridgedInterfaces = list(ifdb.br0.ports.raw)
    if len(bridgedInterfaces) < 2:
        return 1
    firstIf = bridgedInterfaces[0]
    secondIf = bridgedInterfaces[1]
    if ifdb[firstIf].ifname not in ["eth0", "vxlan0"]:
        return 1
    if ifdb[secondIf].ifname not in ["eth0", "vxlan0"]:
        return 1
    if ifdb[firstIf].ifname ==  ifdb[secondIf].ifname:
        return 1
    if ifdb.vxlan0.vxlan_group != str(getTunGW()):
        return 1
    if ifdb.vxlan0.vxlan_id != 42:
        return 1
    if ifdb.vxlan0.vxlan_port != 4789:
        return 1
    return 2

def startOVPN(configFile, username=None, password=None):
    ip = IPDB() 
    ifdb = ip.interfaces
    upfilePath = '/tmp/upfile'

    #Create VPN tunnel
    openvpn_cmd = ['/usr/sbin/openvpn', '--config', configFile, '--daemon', '--writepid', config['PIDFILE']]
    if username != None and password != None:
        with open(upfilePath, 'w') as upfile:
            upfile.write(username+"\n")
            upfile.write(password+"\n")
        os.chmod(upfilePath, 0o400)
        openvpn_cmd.extend(['--auth-user-pass',upfilePath])
    ovpn_process = subprocess.Popen(openvpn_cmd)

    #Wait for openvpn process to die
    ovpn_process.wait()
    os.remove(upfilePath)
    
def waitForTunnelUp(cli=False):
    ip = IPDB() 
    ifdb = ip.interfaces
    #Read openvpn.pid pidfile
    try:
        with open(config['PIDFILE'], "r") as pidfile:
            pid = pidfile.read()
    except:
        return False
    pid = int(pid.strip())
    #Wait for openvpn to create tun interface or to die
    i = 0
    established = False
    while i < config['WAIT_TIME'] and psutil.pid_exists(pid):
        if 'tun0' in ifdb:
            established = True
            break
        time.sleep(1)
        i+= 1
    if not established:
        if not psutil.pid_exists(pid):
            if not cli:
                print("Openvpn Daemon crashed")
        else:
            if not cli:
                print("tun interface couldn't be created after",config['WAIT_TIME'],"seconds")
            choice = None
            if cli:
                return waitForTunnelUp()
            while choice == None:
                choice = input("Should the script exit now? [Y/n]")
                if choice.upper() in ["Y", "YES"]:
                    return False
                elif choice.upper() in ["N", "NO"]:
                    return waitForTunnelUp()
                else:
                    choice = None
        return False
    
    return True
       
def createInterfaces():
    ip = IPDB() 
    ifdb = ip.interfaces
    tunGW = None
    while tunGW == None:
        tunGW = getTunGW()
    
    #Create VXLAN.
    with ip.create(ifname='vxlan0', kind='vxlan', vxlan_id=42, vxlan_group=str(tunGW), vxlan_port=4789) as vxlan:
        vxlan.up()
        
    #Make sure the ethernet interface is up 
    ifdb.eth0.up()
    
    #Create a bridge interface that will bridge the eth0 interface with the vxlan
    with ip.create(kind='bridge', ifname='br0') as br:
        br.add_port(ifdb.eth0)
        br.add_port(ifdb.vxlan0)
        br.up()
    return 0
