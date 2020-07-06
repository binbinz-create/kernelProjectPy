from django.db import models

# Create your models here.

#一些配置信息
class Config:
    ROOT_PASSWD="zhubin123"
    GIT_USER_NAME="jiangdi"
    GIT_PASSWD="jd#180188"
    CREDENTIALS_1="http://"+GIT_USER_NAME+":jd%23180188@172.19.140.200"
    CREDENTIALS_2="https://"+GIT_USER_NAME+":"+GIT_PASSWD+"@172.19.140.200/kernel-management-team/klinux.git"
