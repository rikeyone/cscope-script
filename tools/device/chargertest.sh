#!/bin/sh

if [ -n "$1" ]; then
	pause=$1
else
	pause=3
fi

dump() {
local soc=$(cat /sys/class/power_supply/battery/capacity)
local ac=$(cat /sys/class/power_supply/usb/online)
local usb=$(cat /sys/class/power_supply/pc_port/online)
local time=$(date +%H:%M:%S)
echo "[${time}] ac_online:${ac}, pc_online=${usb}, soc=${soc}"
if [ ${ac} -eq 1 -o ${usb} -eq 1 ];then
	if [ ${soc} -eq 100 ];then
		echo 1 > /sys/class/meizu/charger/cmd_discharging
	fi
else
	if [ ${soc} -eq 3 ];then
		echo 0 > /sys/class/meizu/charger/cmd_discharging
	fi
fi
}

while true
do
	dump
	sleep ${pause}
done
