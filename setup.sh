#!/bin/bash

if [ "$EUID" -ne 0 ] ; then
	echo "You must be root to execute this !"
	exit
fi

echo "The following commands will be executed"
echo "#apt-get update"
echo "#apt-get install openvpn python3 python3-pip"
echo "#pip3 install pyroute2"
echo "#pip3 install netaddr"
echo "#pip3 install psutil"


read -p "Continue ? [y/N]" choix
choix=${choix:-N}

if [ "${choix,,}" != "y" ] ; then
	exit
fi
echo "Starting installation..."

apt-get update -y
apt-get install -y openvpn python3 python3-pip
pip3 install pyroute2
pip3 install netaddr
pip3 install psutil

echo ""
echo ""
echo "The TwinBridge Client has been succcesfully installed on your system. OBSOLETE: To access it, connect to your system via HTTP."
