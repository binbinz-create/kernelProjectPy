import json
import os
import subprocess
from socket import *

from compilekernel.models import Config


#执行命令，并返回打印结果
def exec(command):
    re = os.popen(command).readlines()
    result=[]
    for i in range(0,len(re)):
        result.append(re[i].strip('\n'))
    return result

#实时打印日志
def sh(command, print_msg=True):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.rstrip().decode('utf8')
        if print_msg:
            print(">:", line)
        lines.append(line)
    return lines

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

#专门用来发送编译命令的client
def client_to_server_compile(serverName,command):
    serverPort=12001
    clientSocket=socket(AF_INET,SOCK_DGRAM)
    #发送命令
    clientSocket.sendto(command.encode(),(serverName,serverPort))
    receive_results,serverAddress=clientSocket.recvfrom(16384)
    #将接收到的json字符串转换为list
    results = json.loads(receive_results.decode('utf-8'))
    clientSocket.close()
    return results

#client dedicated to sending pull log commands
def client_to_server_log(serverName,command):
    serverPort=12002
    clientSocket=socket(AF_INET,SOCK_DGRAM)
    #send command
    clientSocket.sendto(command.encode(),(serverName,serverPort))
    receive_results,serverAddress=clientSocket.recvfrom(16384)
    #convert the received json string to a list
    results = json.loads(receive_results.decode('utf-8'))
    clientSocket.close()
    return results

#用于将list转换为dict
def message_list_todict(list):
    compiling_message={}
    compiling_message["cpus"]=list[0];
    compiling_message["user"]=list[1];
    compiling_message["branch"]=list[2];
    compiling_message["version"]=list[3];
    compiling_message["file"]=list[4];
    return compiling_message;


