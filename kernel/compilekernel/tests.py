from django.test import TestCase
import os
from socket import *
import json

import subprocess
#from kernel.compilekernel.utils import exec
# Create your tests here
from kernel.compilekernel.Dao import Dao
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
list_pid =  client_to_server(Config.X86_IP,"ps aux | grep build | awk '{print $2}'")
command = "echo 123123 | sudo -S kill -9 "
for pid in list_pid:
    command+=pid+" "
client_to_server(Config.X86_IP,command)
'''
'''
exec("cd ~/klinux; echo "+Config.ROOT_PASSWD+" | rm -rf build.log ;echo "+Config.ROOT_PASSWD+" | sudo -S  ./scripts/buildpackage.sh  arch/x86/configs/kylin_common.config  >> build.log")
status =  exec("echo $?")
print(status)
'''
'''
command = "cd /tmp/klinux; echo jd#180188 | sudo -S rm -rf build.log ; echo jd#180188 | sudo -S touch build log ; echo jd#180188 | sudo -S chmod 666 build.log ; echo jd#180188 | sudo -S  ./scripts/buildpackage.sh arch/x86/configs/kylin_common.config >> build.log"
results = client_to_server(Config.X86_IP,command)
for log in results:
    print(log)
'''
'''
logs=client_to_server(Config.X86_IP,"ls ~")
for log in logs:
    print(log)
'''
'''
logs = client_to_server("172.19.140.166","ps aux | grep build")
for log in logs:
    print(log)
'''
'''
client_to_server("172.16.31.225","cd /tmp/klinux ;echo zhubin123 | sudo -S rm -rf scripts/tar_kernel.sh")
for command in AfterCompile.commands:
    client_to_server("172.16.31.225","echo zhubin123 |  sudo -S echo \""+command+"\" >> /tmp/klinux/scripts/tar_kernel.sh")
#run tar_kernel.sh and return such as file path , branch version , architecture, suffix , date
results =  client_to_server("172.16.31.225","cd /tmp/klinux/scripts ;echo zhubin123 | sudo -S chmod 777 /tmp/klinux/scripts/tar_kernel.sh ; echo zhubin123 | sudo -S ./tar_kernel.sh")
for log in results:
    print(log)
'''
'''
file_path = "/var/data/ftpdata/robot/2020-08-07_08_54/release-4.4.131-20200805-gc688576ee--package.tar.gz"
paths =  file_path.split("ftpdata")
print(paths[1])
'''
pids =  client_to_server("172.19.140.166", "ps aux | grep build | awk '{print $2}'")
for pid  in pids:
    print(pid)

print("===========")

pids =  client_to_server("172.19.140.166", "ps aux | grep build | awk '$1!~/libvirt+/{print $2}'")
for pid  in pids:
    print(pid)