#!/bin/sh

echo ${USER},${UID}

if [ ! x"${USER}" = x"root" ];then
	echo "Please rerun `basename $0` as root"
	exit 1
else
	echo "Run as root"
fi
