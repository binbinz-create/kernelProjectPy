from django.db import models

# Create your models here.

#一些配置信息
class Config:
    ROOT_PASSWD="zhubin123"
    GIT_USER_NAME="jiangdi"
    GIT_PASSWD="jd#180188"
    CREDENTIALS_1="http://"+GIT_USER_NAME+":jd%23180188@172.19.140.200"
    CREDENTIALS_2="https://"+GIT_USER_NAME+":"+GIT_PASSWD+"@172.19.140.200/kernel-management-team/klinux.git"

class AfterCompile:
    commands=["SUFFIX=`cat debian/build/build-generic/.config | grep LOCALVERSION= | awk -F'\"' '{print $2}' | awk -F'.' '{print $3}'` ; echo ${SUFFIX}",
              "VERSION=`cat Makefile  | grep VERSION | head -n 1 | awk -F' = ' '{print $2}'` ",
              "PATCHLEVEL=`cat Makefile  | grep PATCHLEVEL | head -n 1 | awk -F' = ' '{print $2}'`",
              "SUBLEVEL=`cat Makefile  | grep SUBLEVEL | head -n 1 | awk -F' = ' '{print $2}'`",
              "EXTRAVERSION=`cat Makefile | grep \"EXTRAVERSION =\" | head -n 1 | awk -F'-'  '{print $2}'`",
              "GIT_VERSION=`git log --oneline  | head -n 1  | awk -F' ' '{print $1}'`",
              "KERNEL_VERSION=${VERSION}.${PATCHLEVEL}.${SUBLEVEL}-${EXTRAVERSION}-g${GIT_VERSION}",
              "DATE=`date '+%Y-%m-%d_%H_%M'`",
              "tar -zcvf \"release-${KERNEL_VERSION}-${SUFFIX}-package.tar.gz\" ../*deb",
              "rm -rf ../*deb",
              "mkdir -p /var/data/ftpdata/robot/${DATE}/",
              "mv release-${KERNEL_VERSION}-${SUFFIX}-package.tar.gz /var/data/ftpdata/robot/${DATE}/"
              ]
    pass