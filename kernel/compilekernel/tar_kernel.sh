#!/bin/bash
ARCHITECTURE=`uname -m`
SUFFIX=`cat debian/build/build-generic/.config | grep LOCALVERSION= | awk -F'"' '{print $2}' | awk -F'.' '{print $3}'`
VERSION=`cat Makefile  | grep VERSION | head -n 1 | awk -F' = ' '{print $2}'`
PATCHLEVEL=`cat Makefile  | grep PATCHLEVEL | head -n 1 | awk -F' = ' '{print $2}'`
SUBLEVEL=`cat Makefile  | grep SUBLEVEL | head -n 1 | awk -F' = ' '{print $2}'`
EXTRAVERSION=`cat Makefile | grep "EXTRAVERSION =" | head -n 1 | awk -F'-'  '{print $2}'`
GIT_VERSION=`git log --oneline  | head -n 1  | awk -F' ' '{print $1}'`
KERNEL_VERSION=${VERSION}.${PATCHLEVEL}.${SUBLEVEL}-${EXTRAVERSION}-g${GIT_VERSION}
BRANCH_VERSION=`git branch | grep "\*" | awk -F'*' '{print $2}' | sed 's/^.//g'`
DATE=`date '+%Y-%m-%d_%H_%M'`
tar -zcvf "release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz" ../*deb
#rm -rf ../*deb
echo $1 | sudo -S mkdir -p /var/data/ftpdata/robot/${DATE}/
echo $1 | sudo -S mv release-${KERNEL_VERSION}-${SUFFIX}-package.tar.gz /var/data/ftpdata/robot/${DATE}/
echo var/data/ftpdata/robot/\${DATE}/release-\${KERNEL_VERSION}-\${SUFFIX}-package.tar.gz
echo ${KERNEL_VERSION}
echo ${ARCHITECTURE}
echo ${SUFFIX}
echo ${BRANCH_VERSION}
echo $(date '+%Y-%m-%d_%H_%M')
