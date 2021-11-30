#!/bin/sh

ip link del br0
ip link del vxlan0
DIR=$(cd `dirname $0` && pwd)
killall openvpn
rm $DIR/openvpn.pid
