#!/bin/bash

tar -zxvf git-lfs-linux-amd64-v2.7.2.tar.gz
sudo ./install.sh

git lfs track "*.zip"
git lfs track "*.tar.gz"
git lfs track "*.tgz"
