#!/bin/bash

if [ "$EUID" -ne 0 ] ; then
	echo "You must be root to execute this !"
	exit
fi

echo "Starting installation..."



echo ""
echo ""
echo "The TwinBridge Client has been succcesfully installed on your system."
