sudo apt-get install nfs-common
sudo apt-get install cifs-utils

sudo mount -t cifs -o username="xhc",password="123456",domain="MEIZU",rw,uid=1000,gid=1000 //dailybuild2/firmware/DailyBuild4Test /media/cloud/dailybuild2/
sudo mount -t ntfs -o gid="1000",uid="1000",iocharset=utf8,rw,dir_mode=0666,file_mode=0777 /dev/sdf1  /media/xiehaocheng/seagate
