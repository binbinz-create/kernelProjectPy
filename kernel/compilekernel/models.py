from django.db import models

# Create your models here.

#一些配置信息
class Config:
    ROOT_PASSWD="zhubin123"
    #X86_ROOT_PASSWD="jd#180188"
    X86_ROOT_PASSWD="zhubin123"
    ARM_ROOT_PASSWD="jd#180188"
    MIPS_ROOT_PASSWD="123123"
    GIT_ADDRESS="http://172.19.140.200/jiangdi/klinux.git"
    GIT_USER_NAME="jiangdi"
    GIT_PASSWD="jd#180188"
    CREDENTIALS_1="http://"+GIT_USER_NAME+":jd%23180188@172.19.140.200"
    CREDENTIALS_2="https://"+GIT_USER_NAME+":"+GIT_PASSWD+"@172.19.140.200/jiangdi/klinux.git"
    ARM_IP="172.19.140.198"
    #X86_IP="172.19.140.166"
    X86_IP="172.16.31.225"
    MIPS_IP="172.19.140.199"


#编译完成之后的打包操作,shell ,参照release...
class AfterCompile:
    commands=["#!/bin/bash",
              "SUFFIX=`cd /tmp/klinux ; cat debian/build/build-generic/.config | grep LOCALVERSION= | awk -F'\"' '{print $2}' | awk -F'.' '{print $3}'` ",
              "VERSION=`cd /tmp/klinux ;cat Makefile  | grep VERSION | head -n 1 | awk -F' = ' '{print $2}'` ",
              "PATCHLEVEL=`cd /tmp/klinux ;cat Makefile  | grep PATCHLEVEL | head -n 1 | awk -F' = ' '{print $2}'`",
              "ARCHITECTURE=`uname -m`",
              "SUBLEVEL=`cd /tmp/klinux ;cat Makefile  | grep SUBLEVEL | head -n 1 | awk -F' = ' '{print $2}'`",
              "EXTRAVERSION=`cd /tmp/klinux ;cat Makefile | grep \"EXTRAVERSION =\" | head -n 1 | awk -F'-'  '{print $2}'`",
              "GIT_VERSION=`cd /tmp/klinux ;git log --oneline  | head -n 1  | awk -F' ' '{print $1}'`",
              "KERNEL_VERSION=\${VERSION}.\${PATCHLEVEL}.\${SUBLEVEL}-\${EXTRAVERSION}-g\${GIT_VERSION}",
              "BRANCH_VERSION=\$(git branch | grep \"\"\\*\"\" | awk -F'*' '{print \$2}' | sed 's/^.//g')",
              "DATE=\$(date '+%Y-%m-%d_%H_%M')",
              "tar -zcvf \"release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz\" ../*deb",
              "rm -rf ../*deb",
              "mkdir -p /var/data/ftpdata/robot/\${DATE}/",
              "mv release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz /var/data/ftpdata/robot/\${DATE}/",
              #outputs the path of the compiled and packaged kernel package, kernel_version, architecture,suffix, branch_version for recoding
              "echo /var/data/ftpdata/robot/\${DATE}/release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz",
              "echo \${KERNEL_VERSION}",
              "echo \${ARCHITECTURE}",
              "echo \${SUFFIX}",
              "echo \${BRANCH_VERSION}",
              "echo \$(date '+%Y-%m-%d_%H_%M')"
              ]
    pass