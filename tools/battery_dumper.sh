#!/bin/sh
let count=0
local utime
local ktime
local pause_time=1
if [ -n "$1" ]; then
pause_time=$1
fi
dump_peripheral () {
local time=$(date +%H:%M:%S)
local curr=$(cat /sys/class/power_supply/battery/current_now)
local volt=$(cat /sys/class/power_supply/battery/voltage_now)
local soc=$(cat /sys/class/power_supply/battery/capacity)
echo "[${time}] volt:${volt}, curr=${curr}, soc=${soc}"
}
echo "Starting capture!"
echo "pause time = $pause_time"

while true
do
utime=($(cat /proc/uptime))
ktime=${utime[0]}
dump_peripheral ${ktime}
let count=$count+1
sleep $pause_time
done
