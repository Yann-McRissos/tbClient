#!/bin/python3
import sys
from pyroute2 import IPRoute
import requests, os, sys, subprocess, time


def buildTopology(configFile):
    ip = IPRoute() 
    
    #Create VPN tunnel
    openvpn_cmd = ['/usr/sbin/openvpn', '--config', vpn_config, '--daemon']
    ovpn_process = subprocess.Popen(openvpn_cmd)

    tun_index = ip.link_lookup(ifname='tun0')
    while len(tun_index) == 0:
        time.sleep(1)
        tun_index = ip.link_lookup(ifname='tun0') 
        #If the process has terminated with 1 it means it didn't connect properly.
        if ovpn_process.returncode == 1:
            return 1
    
    vpn_address = ip.get_addr(index=tun_index)
    #Create multicast VXLAN. MC traffic goes through the established tunnel
    ip.link('add', ifname='vxlan0', kind='vxlan', vxlan_id=42, vxlan_group='172.16.100.1', vxlan_port=4789)

    #Bridges the Eth0 int with the created VXLAN
    ip.link('add', ifname='br0', kind='bridge')
    eth_index = ip.link_lookup(ifname='eth0')
    vxlan_index = ip.link_lookup(ifname='vxlan0')
    bridge_index = ip.link_lookup(ifname='br0')
    ip.link('set', index=bridge_index, state='up')
    ip.link('set', index=vxlan_index, state='up')
    ip.link('set', index=eth_index, master=bridge_index)
    ip.link('set', index=vxlan_index, master=bridge_index)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give only the name of the config file as argument")
        sys.exit(1)    
    vpn_config = sys.argv[1]
    buildTopology(vpn_config)   
