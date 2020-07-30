from django.test import TestCase
import os
from socket import *
import json

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

#免用户名和密码登录git
def git_without_passwd(serverName):
    client_to_server(serverName,"echo "+Config.CREDENTIALS_1+" > ~/.git-credentials")
    client_to_server(serverName,"echo "+Config.CREDENTIALS_2+" >> ~/.git-credentials")
    client_to_server(serverName,"git config --global credential.helper store")

#向serverName发送命令command
def client_to_server(serverName,command):
    serverPort=12000
    clientSocket=socket(AF_INET,SOCK_DGRAM)
    #发送命令
    clientSocket.sendto(command.encode(),(serverName,serverPort))
    receive_results,serverAddress=clientSocket.recvfrom(16384)
    #将接收到的json字符串转换为list
    results = json.loads(receive_results.decode('utf-8'))
    clientSocket.close()
    return results

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
#杀死进程
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

git_without_passwd(Config.MIPS_IP)
results =  client_to_server(Config.MIPS_IP,"echo 123123 | sudo -S git clone " + Config.GIT_ADDRESS+ " /tmp/klinux")
