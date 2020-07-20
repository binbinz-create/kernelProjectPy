from django.test import TestCase
import os
import subprocess
#from kernel.compilekernel.utils import exec
# Create your tests here


def exec(command):
    re = os.popen(command).readlines()
    result=[]
    for i in range(0,len(re)):
        result.append(re[i].strip('\n'))
    return result


'''
SUFFIX=`cat debian/build/build-generic/.config | grep LOCALVERSION= | awk -F'"' '{print $2}' | awk -F'.' '{print $3}'`
VERSION=`cat Makefile  | grep VERSION | head -n 1 | awk -F' = ' '{print $2}'`
PATCHLEVEL=`cat Makefile  | grep PATCHLEVEL | head -n 1 | awk -F' = ' '{print $2}'`
SUBLEVEL=`cat Makefile  | grep SUBLEVEL | head -n 1 | awk -F' = ' '{print $2}'`
EXTRAVERSION=`cat Makefile | grep "EXTRAVERSION =" | head -n 1 | awk -F'-'  '{print $2}'`

GIT_VERSION=`git log --oneline  | head -n 1  | awk -F' ' '{print $1}'`
KERNEL_VERSION=${VERSION}.${PATCHLEVEL}.${SUBLEVEL}-${EXTRAVERSION}-g${GIT_VERSION}

'''

command = "asdfasdf"
print(command[:-1])