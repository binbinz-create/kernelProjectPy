from django.test import TestCase
import os
import subprocess
#from kernel.compilekernel.utils import exec
# Create your tests here
from kernel.compilekernel.models import AfterCompile, Config

def exec(command):
    re = os.popen(command).readlines()
    result=[]
    for i in range(0,len(re)):
        result.append(re[i].strip('\n'))
    return result

'''
results = exec("cd ~/klinux ; ./tar_kernel.sh")
print(results[-6]) #下载链接
print(results[-5]) #主线版本
print(results[-4]) #应用结构
print(results[-3]) #个性版本
print(results[-2]) #分支版本
print(results[-1]) #时间
print(results[-6].split('/')[-1]) #package name
'''

'''
list_pid =  exec("ps aux | grep build | awk '{print $2}'")
command = "echo zhubin123 | sudo -S kill -9 "
for pid in list_pid:
    command+=pid+" "
exec(command)
'''

'''
exec("cd ~/klinux; echo "+Config.ROOT_PASSWD+" | rm -rf build.log ;echo "+Config.ROOT_PASSWD+" | sudo -S  ./scripts/buildpackage.sh  arch/x86/configs/kylin_common.config  >> build.log")
status =  exec("echo $?")
print(status)
'''

deb_num = exec("ls -l ~/*deb | wc -l")[0]
print(deb_num)