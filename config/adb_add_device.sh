#!/bin/sh

if [ $# != 2 ]; then
	echo "usage: $0 vendorid productid"
	exit 1
fi

#if [ ! x${USER} = x"root" ]; then
#	echo "rerun it as root!!!"
#	exit 1;
#fi

echo $1 >> ~/.android/adb_usb.ini
sudo echo \
	"SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"$1\", ATTRS{idProduct}==\"$2\", MODE=\"0666\"" \
>> /etc/udev/rules.d/51-android.rules
sudo chmod a+x /etc/udev/rules.d/51-android.rules
sudo service udev restart
