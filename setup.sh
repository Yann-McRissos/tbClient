#!/bin/bash

if [ "$EUID" -ne 0 ] ; then
	echo "Le script doit être exécuté en tant que root!"
	exit
fi

echo "Les commandes suivantes vont être exécutées"
echo "#apt-get update"
echo "#apt-get install openvpn python3 python3-pip"
echo "#pip3 install git+https://github.com/svinota/pyroute2/"
echo "#pip3 install netaddr"
echo "#pip3 install psutil"

read -p "Etes-vous d'accord? [y/N]" choix
choix=${choix:-N}

if [ "${choix,,}" != "y" ] ; then
	exit
fi
echo "Installation..."

apt-get update -y
apt-get install -y openvpn python3 python3-pip
pip3 install git+https://github.com/svinota/pyroute2/
pip3 install netaddr
pip3 install psutil

echo ""
echo ""
echo "TwinBridge Client a été installé sur votre Raspberry Pi. Pour y accéder, connectez-vous en HTTP sur votre Raspberry Pi."


