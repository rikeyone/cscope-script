#!/bin/bash

i=0
configs=($(ls arch/arm64/configs/*))
#echo ${configs[@]}

for file in ${configs[@]}
do
	echo ${i}:${file##*/};
	((i++));
done

echo please input your choice:
read choice

target=${configs[${choice}]##*/}

echo target is: ${target}

sleep 5

case $choice in
	*) echo "good";;
esac

if [ -d `pwd`/out ]
then
	rm `pwd`/out -rf;mkdir `pwd`/out
else
	mkdir `pwd`/out
fi

make ARCH=arm64 CROSS_COMPILE=aarch64-linux-android- O=`pwd`/out $target
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-android- O=`pwd`/out -j8
