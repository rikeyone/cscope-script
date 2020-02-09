#!/bin/sh


if [ ! x"${USER}" = x"root" ];then
	echo "Please rerun `basename $0` as root!!!"
	exit 1
fi

echo ${USER}

## >>>>>>>>>>>>>>>>>>>> below is for develop environment software <<<<<<<<<<<<<<<<<<<<<<

## essiential
sudo apt-get install vim cscope ctags
sudo apt-get install build-essential
sudo apt-get install tree
sudo apt-get install cmake
cp config/.vimrc ~/.vimrc

## add cscope tool developed by myself
sudo cp config/cscope.sh /usr/local/bin/
echo "alias setcs='cscope.sh && export CSCOPE_DB=\`pwd\`/cscope.out'" >> ~/.bashrc

## git
## Note: you should copy your .gitconfig and .ssh 
## before install new version of ubuntu!!!
sudo apt install git git-email gitk

## For gerrit commit config
#sudo cp config/gitinit.py /usr/local/bin/
sudo cp config/repo /usr/local/bin/
sudo cp config/commit-msg  /usr/share/git-core/templates/hooks/
cp config/.gitconfig ~/.gitconfig

## minicom
sudo apt-get install minicom

## jdk8
sudo apt-get install openjdk-8-jdk

## fastboot & adb
sudo apt-get install android-tools-fastboot
sudo apt-get install android-tools-adb

## use this script to install usb device for adb
# SUBSYSTEM=="usb", ATTRS{idVendor}=="2a45", ATTRS{idProduct}=="0c02",MODE="0666"
# Set USB device mode, other wise you must use sudo command.
sudo cp config/adb_add_device.sh /usr/local/bin/

## QCOM QFIL Mode using /dev/ttyUSB* device
## so we need to set the device mode to 0666
sudo usermod -aG plugdev $LOGNAME
echo 'KERNEL=="ttyUSB[0-9]*", MODE="0666"' > 70-ttyusb.rules
sudo mv 70-ttyusb.rules /etc/udev/rules.d/70-ttyusb.rules

## EDK2 build
sudo apt-get install build-essential uuid-dev nasm

## Android compile library
sudo apt-get install gnupg flex bison gperf zip curl zlib1g-dev zlib1g-dev:i386 gcc-multilib g++-multilib libc6-dev libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z1-dev ccache libgl1-mesa-dev libgl1-mesa-glx:i386 libxml2-utils xsltproc unzip lib32z1 libncurses5-dev:i386 libx11-dev:i386 libreadline6-dev:i386  tofrodos python-markdown libssl-dev device-tree-compiler

## NFS cifs mount
sudo apt-get install nfs-common
sudo apt-get install cifs-utils

# For Andorid O/P or later
#1.sudo apt-get install libxml-simple-perl
#2.perl -e shell -MCPAN
#3.install XML::Parser
echo "WARNING: For Andord O/P or later, need to install libxml like below:"
echo "1.sudo apt-get install libxml-simple-perl"
echo "2.perl -e shell -MCPAN"
echo "3.install XML::Parser"
echo "> Install development environment successfully! <"

## >>>>>>>>>>>>>>>>>>>> below is for ubuntu software <<<<<<<<<<<<<<<<<<<<<<

echo "Do you want to continue installing ubuntu software(virtulbox/meld/chrome/wiznote...)? (y/n)"
read choice
if [ "$choice" = "n" ]; then
    exit 0
fi

## virtulbox
echo "Do you want to install virtualbox? (y/n)"
read choice
if [ "$choice" = "n" ]; then
    echo "do not install virtualbox"
else
    echo "install virtualbox"
	sudo apt-get install virtualbox
fi

## compare tool
echo "Do you want to install meld compare tool? (y/n)"
read choice
if [ "$choice" = "n" ]; then
    echo "do not install meld"
else
    echo "install meld"
	sudo apt-get install meld
fi

## chromium-browser
echo "Do you want to install chromium-browser? (y/n)"
read choice
if [ "$choice" = "n" ]; then
    echo "do not install chromium-browser"
else
    echo "install chromium-browser"
	sudo apt-get install chromium-browser
fi

## AppImageLauncher
echo "Do you want to install AppImageLauncher? (y/n)"
read choice
if [ x$choice != xn ]; then
	echo "what is your ubuntu version: (1/2/3)"
	echo "1: 16.04 "
	echo "2: 18.04 "
	echo "3: other "
	read version
	if [ "$version" = "1" ]; then
		# ubuntu 16.04
		wget -O appimagelauncher.deb \
		"https://github.com/TheAssassin/AppImageLauncher/releases/download/continuous/appimagelauncher_1.3.1-travis683.git20190708.38ad3be.xenial_amd64.deb"
		chmod a+x appimagelauncher.deb
		sudo dpkg -i appimagelauncher.deb
	elif [ "$version" = "2" ]; then
		# ubuntu 18.04
		wget -O appimagelauncher.deb \
		"https://github.com/TheAssassin/AppImageLauncher/releases/download/continuous/appimagelauncher_1.2.2-travis556.git20190414.ba13bec.bionic_amd64.deb"
		chmod a+x appimagelauncher.deb
		sudo dpkg -i appimagelauncher.deb
	else
		echo "do not support this ubuntu version!"
	fi
else
    echo "do not install AppImageLauncher"
fi

## WizNote
echo "Do you want to install WizNote? (y/n)"
read choice
if [ x$choice != xn ]; then
	echo "what is your ubuntu version: (1/2/3)"
	echo "1: 16.04 "
	echo "2: 18.04 "
	echo "3: other "
	read version
	if [ "$version" = "1" ]; then
		# WizNote 16.04 ppa source
		sudo add-apt-repository ppa:wiznote-team
		sudo apt-get update
		sudo apt-get install wiznote
	elif [ "$version" = "2" ]; then
		# ubuntu 18.04
		wget "https://github.com/altairwei/WizNotePlus/releases/download/v2.7.0/WizNote-x86_64.AppImage"
		chmod 777 WizNote-x86_64.AppImage
		sudo cp WizNote-x86_64.AppImage /usr/local/bin/
	else
		echo "do not support this ubuntu version!"
	fi
else
    echo "do not install WizNote"
fi

## pdf reader
#sudo apt-get install okular
