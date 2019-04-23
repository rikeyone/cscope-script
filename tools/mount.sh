sudo apt-get install cifs-utils
sudo mount -t cifs -o username="xhc",password="123456",gid="1000",uid="1000",iocharset=utf8,rw,dir_mode=0777,file_mode=0777 //172.20.20.20/share  /media/cloud/bsplogshare/
sudo mount -t ntfs -o gid="1000",uid="1000",iocharset=utf8,rw,dir_mode=0666,file_mode=0777 /dev/sdf1  /media/xiehaocheng/seagate
