import os
import subprocess
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
def git_without_passwd():
    os.system("echo "+Config.CREDENTIALS_1+" > ~/.git-credentials")
    os.system("echo "+Config.CREDENTIALS_2+" >> ~/.git-credentials")
    os.system("git config --global credential.helper store")

