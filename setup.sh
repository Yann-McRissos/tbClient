#!/bin/bash

if [ "$EUID" -ne 0 ] ; then
	echo "Le script doit être exécuté en tant que root!"
	exit
fi

echo "Les commandes suivantes vont être exécutées"
echo "#apt-get update"
echo "#apt-get install openvpn python3 python3-pip"
echo "#pip3 install pyroute2"
echo "#pip3 install netaddr"
echo "#pip3 install psutil"
echo "#mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bak"
echo "#cp configs/dhcpcd.conf /etc/dhcpcd.conf"
echo "#systemctl restart dhcpcd"

read -p "Etes-vous d'accord? [N]" choix
choix=${choix:-N}

if [ "${choix,,}" != "y" ] ; then
	exit
fi
echo "Installation..."

apt-get update -y
apt-get install -y openvpn python3 python3-pip
pip3 install pyroute2
pip3 install netaddr
pip3 install psutil

echo ""
echo ""
echo "Sauvegarde du fichier dhcpcd.conf..."
mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bak
echo "Installation d'une nouvelle configuration dhcpcd"
cp configs/dhcpcd.conf /etc/dhcpcd.conf
echo "Redemarrage de dhcpcd"
systemctl restart dhcpcd
echo ""
echo ""
echo ""
echo ""
echo "La connexion au serveur peut être établie en lancant le script suivant: "
echo "   sudo python3 buildTopology.py"
echo ""
echo "Pour fermer la connexion vers le serveur :"
echo "   sudo sh flush.sh"
echo ""
echo ""


