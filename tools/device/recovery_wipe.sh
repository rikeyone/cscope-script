#!/bin/sh
echo --wipe_all > /cache/recovery/command
if [ $? -ne 0 ];then
echo write --wipe_all command error > /sdcard/test.log
exit 1
fi
echo --reason=recoverytest >> /cache/recovery/command
if [ $? -ne 0 ];then
echo write --reason command error > /sdcard/test.log
exit 1
fi
sync
reboot recovery

