#!/bin/bash

## android platform tools
unzip platform-tools_r27.0.1-linux.zip
sudo cp -a platform-tools /opt/

## set alias for systrace script
echo "alias st-start='python /opt/platform-tools/systrace/systrace.py'" \
>> ~/.bashrc

echo "alias st-start-gfx='st-start -t 8 gfx input view sched freq wm am hwui workq res dalvik sync disk load perf hal rs idle mmc'" \
>> ~/.bashrc

echo "alias st-start-simple='st-start --time=10 sched gfx view wm'" \
>> ~/.bashrc

