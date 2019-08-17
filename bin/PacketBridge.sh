#!/bin/bash
java -jar /etc/tbClient/bin/PacketBridge.jar >/tmp/packetbridgeout 2>&1 $@ &
sleep 3
if [[ `grep -c "No route to host" /tmp/packetbridgeout`  != 0 ]]; then
	echo "firewallerror"
fi
rm /tmp/packetbridgeout
echo $!

