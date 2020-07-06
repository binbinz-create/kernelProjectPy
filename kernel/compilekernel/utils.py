import os
from compilekernel.models import Config

#执行命令，并返回打印结果
def exec(command):
    re = os.popen(command).readlines()
    result=[]
    for i in range(0,len(re)):
        result.append(re[i].strip('\n'))
    return result

#免用户名和密码登录git
def git_without_passwd():
    os.system("echo "+Config.CREDENTIALS_1+" > ~/.git-credentials")
    os.system("echo "+Config.CREDENTIALS_2+" >> ~/.git-credentials")
    os.system("git config --global credential.helper store")

