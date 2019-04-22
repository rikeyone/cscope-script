#!/bin/bash
count=0
adb root
if [ $? -eq 0 ]
then
	while [ ${count} -lt 10000 ]
	do
		((count++))
		adb shell cat /sys/class/power_supply/battery/status
		sleep 0.2
	done
fi
