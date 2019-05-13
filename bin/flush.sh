#!/bin/sh

ip link del br0
ip link del vxlan0
DIR=$(cd `dirname $0` && pwd)
pkill -F $DIR/openvpn.pid
rm $DIR/openvpn.pid
