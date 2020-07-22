from django.test import TestCase
import os
import subprocess
#from kernel.compilekernel.utils import exec
# Create your tests here
from kernel.compilekernel.models import AfterCompile


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

os.system("cd ~/klinux ; rm -rf tar_kernel.sh")
for command in AfterCompile.commands:
    os.system("echo \"" + command + "\" >> ~/klinux/tar_kernel.sh")
results = exec("cd ~/klinux ; chmod 777 ~/klinux/tar_kernel.sh ;  ./tar_kernel.sh")
