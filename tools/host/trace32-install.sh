#!/bin/bash

if [ $# -lt 1 ]; then
	echo "Please enter the trace32 CDROM-DIR as arg1!"
	exit 1
fi

sudo mkdir /opt/t32
sudo cp -r $1/files/* /opt/t32/
sudo cp /opt/t32/demo/practice/t32.cmm /opt/t32/
sudo cp /opt/t32/bin/pc_linux64/filecvt /opt/t32/
#install PDF viewer(not need in my case)
#install font( QT UI not need which is my case)

#setting of TRACE32 environment variables
echo "export T32SYS=/opt/t32" >> ~/.bashrc
echo "export T32TMP=/tmp" >> ~/.bashrc
echo "export T32ID=T32" >> ~/.bashrc
echo "export PATH=$PATH:/opt/t32/bin/pc_linux64" >> ~/.bashrc
