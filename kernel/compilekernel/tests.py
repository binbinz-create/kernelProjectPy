from django.test import TestCase
import os
import subprocess
# Create your tests here
'''
re = os.popen("ls -l").readlines()
for i in range(0,len(re)-1):
    print(re[i].strip('\n'))
'''
def sh(command, print_msg=True):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.rstrip().decode('utf8')
        if print_msg:
            print(">>>", line)
        lines.append(line)
    return lines

sh("cd ~/klinux; ./scripts/buildpackage.sh arch/x86/configs/kylin_common.config")