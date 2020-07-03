from django.test import TestCase
import os
# Create your tests here

re = os.popen("ls -l").readlines()
for i in range(0,len(re)-1):
    print(re[i].strip('\n'))

