#!/bin/sh


if [ ! x"${USER}" = x"root" ];then
	echo "Please rerun `basename $0` as root!!!"
	exit 1
fi

echo ${USER}

## essiential
sudo apt-get install vim cscope ctags
sudo apt-get install build-essential
sudo apt-get install tree
sudo apt-get install cmake
cp config/.vimrc ~/.vimrc

## add cscope tool developed by myself
sudo cp config/cscope.sh /usr/local/bin/
echo "alias cscope='source /usr/local/bin/cscope.sh'" >> ~/.bashrc

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

## chromium-browser
sudo apt-get install chromium-browser

## pdf reader
#sudo apt-get install okular

## AppImageLauncher
wget -O appimagelauncher.deb \
	"https://github.com/TheAssassin/AppImageLauncher/releases/download/continuous/appimagelauncher_1.2.2-travis556.git20190414.ba13bec.bionic_amd64.deb"
chmod a+x appimagelauncher.deb
sudo ./appimagelauncher.deb &

## WizNote
wget "https://github.com/altairwei/WizNotePlus/releases/download/v2.7.0/WizNote-x86_64.AppImage"
chmod 777 WizNote-x86_64.AppImage
sudo cp WizNote-x86_64.AppImage /usr/local/bin/

## jdk8
sudo apt-get install openjdk-8-jdk

## fastboot & adb
sudo apt-get install android-tools-fastboot
sudo apt-get install android-tools-adb
echo 'KERNEL=="ttyUSB[0-9]*", MODE="0666"' > 70-ttyusb.rules
sudo mv 70-ttyusb.rules /etc/udev/rules.d/70-ttyusb.rules

## use this script to install usb device for adb
sudo cp config/adb_add_device.sh /usr/local/bin/

## virtulbox
sudo apt-get install virtualbox

## compare tools
sudo apt-get install meld

## EDK2 build
sudo apt-get install build-essential uuid-dev nasm

## Android compile library
sudo apt-get install gnupg flex bison gperf zip curl zlib1g-dev zlib1g-dev:i386 gcc-multilib g++-multilib libc6-dev libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z1-dev ccache libgl1-mesa-dev libgl1-mesa-glx:i386 libxml2-utils xsltproc unzip lib32z1 libncurses5-dev:i386 libx11-dev:i386 libreadline6-dev:i386  tofrodos python-markdown libssl-dev device-tree-compiler

# For Andorid O/P or later
#1.sudo apt-get install libxml-simple-perl
#2.perl -e shell -MCPAN
#3.install XML::Parser
