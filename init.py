#!/bin/python3
import sys
from pyroute2 import IPRoute
import requests, os, sys, subprocess, time

ip = IPRoute() 

if len(sys.argv) != 2:
    print("Please give only the name of the config file as argument")
    sys.exit(1)

#Create VPN tunnel
vpn_config = sys.argv[1]
openvpn_cmd = ['/usr/sbin/openvpn', '--config', vpn_config, '--daemon']
ovpn_process = subprocess.Popen(openvpn_cmd)

tun_index = ip.link_lookup(ifname='tun0')
while tun_index == []:
    time.sleep(1)
    tun_index = ip.link_lookup(ifname='tun0') 

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
