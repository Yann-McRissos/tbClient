#!/usr/bin/python3
import sys
from pyroute2 import IPDB # pip3 install pyroute2
import requests, os, sys, subprocess, time
from netaddr import * # pip3 install netaddr
from includes.methods import * 

def buildTopology(configFile, username=None,
        password=None):
    ip = IPDB() 
    ifdb = ip.interfaces
    upfilePath = '/tmp/upfile'

    #If tun0 already exists the VPN is already running.
    if 'tun0' in ifdb:
        print("A tun0 interface already exists")
        return 1

    #Create VPN tunnel
    openvpn_cmd = ['/usr/sbin/openvpn', '--config', configFile, '--daemon']
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
    #Wait for openvpn to create tun interface
    i = 0
    while 'tun0' not in ifdb:
        if i > 10:
            print("tun interface couldn't be created after 10 seconds. It looks like it crashed...")
            return 1
        time.sleep(1)
        i+= 1

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

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("Please give only the name of the config file and credentials as arguments")
        sys.exit(1)    
    
    vpn_config = sys.argv[1]
    if len(sys.argv) == 4:
        username = sys.argv[2]
        password = sys.argv[3]
        buildTopology(vpn_config, username, password)
    else:
        buildTopology(vpn_config)   
