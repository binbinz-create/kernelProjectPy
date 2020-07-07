from django.test import TestCase
import os
import subprocess
from compilekernel.utils import exec
# Create your tests here
'''
re = os.popen("ls -l").readlines()
for i in range(0,len(re)-1):
    print(re[i].strip('\n'))
'''

'''
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
'''

#测试返回日志和行号
l = exec("cd ~/klinux ; tail +0 build.log ; wc -l build.log")
num =  l[-1].split(' ')[0]  #切出行号
l_nonu = l[:-1]   #将行号切掉
for item in l_nonu:
    print(item)

