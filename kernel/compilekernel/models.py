from django.db import models

# Create your models here.

#一些配置信息
class Config:
    ROOT_PASSWD="zhubin123"
    GIT_USER_NAME="jiangdi"
    GIT_PASSWD="jd#180188"
    CREDENTIALS_1="http://"+GIT_USER_NAME+":jd%23180188@172.19.140.200"
    CREDENTIALS_2="https://"+GIT_USER_NAME+":"+GIT_PASSWD+"@172.19.140.200/kernel-management-team/klinux.git"

#编译完成之后的打包操作,shell ,参照release...
class AfterCompile:
    commands=["#!/bin/bash",
              "SUFFIX=`cd ~/klinux ; cat debian/build/build-generic/.config | grep LOCALVERSION= | awk -F'\"' '{print $2}' | awk -F'.' '{print $3}'` ",
              "VERSION=`cd ~/klinux ;cat Makefile  | grep VERSION | head -n 1 | awk -F' = ' '{print $2}'` ",
              "PATCHLEVEL=`cd ~/klinux ;cat Makefile  | grep PATCHLEVEL | head -n 1 | awk -F' = ' '{print $2}'`",
              "ARCHITECTURE=`uname -m`",
              "SUBLEVEL=`cd ~/klinux ;cat Makefile  | grep SUBLEVEL | head -n 1 | awk -F' = ' '{print $2}'`",
              "EXTRAVERSION=`cd ~/klinux ;cat Makefile | grep \"EXTRAVERSION =\" | head -n 1 | awk -F'-'  '{print $2}'`",
              "GIT_VERSION=`cd ~/klinux ;git log --oneline  | head -n 1  | awk -F' ' '{print $1}'`",
              "KERNEL_VERSION=\${VERSION}.\${PATCHLEVEL}.\${SUBLEVEL}-\${EXTRAVERSION}-g\${GIT_VERSION}",
              "BRANCH_VERSION=\$(git branch | grep \"\"\\*\"\" | awk -F'*' '{print \$2}' | sed 's/^.//g')",
              "echo " +Config.ROOT_PASSWD+ " | sudo -S ntpdate -u ntp1.aliyun.com",
              "DATE=\$(date '+%Y-%m-%d_%H_%M')",
              "tar -zcvf \"release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz\" ../*deb",
              "rm -rf ../*deb",
              "echo "+Config.ROOT_PASSWD+" | sudo -S mkdir -p /var/data/ftpdata/robot/\${DATE}/",
              "echo "+Config.ROOT_PASSWD+" | sudo -S mv release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz /var/data/ftpdata/robot/\${DATE}/",
              #outputs the path of the compiled and packaged kernel package, kernel_version, architecture,suffix, branch_version for recoding
              "echo /var/data/ftpdata/robot/\${DATE}/release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz",
              "echo \${KERNEL_VERSION}",
              "echo \${ARCHITECTURE}",
              "echo \${SUFFIX}",
              "echo \${BRANCH_VERSION}",
              "echo \$(date '+%Y-%m-%d_%H_%M')"
              ]
    pass