#!/bin/sh
ip link del br0
ip link del vxlan0
#killall openvpn
pkill -F openvpn.pid
rm openvpn.pid
