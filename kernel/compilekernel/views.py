
import os
from django.shortcuts import render
from compilekernel.utils import git_without_passwd
from compilekernel.utils import exec
from compilekernel.models import Config,AfterCompile
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

#直接跳转到index.html页面
def to_index(request):
    return render(request, "compilekernel/index.html", None)


#直接跳转到test.html页面
def to_test(request):
    return render(request,"compilekernel/test.html",None)


#列出配置文件的请求
def file_list(request):
    cpus = request.GET.get("cpus")
    branch = request.GET.get("branch")
    #免用户名和密码即可操作git
    git_without_passwd()
    #切换分支，更新资源
    exec("cd ~/klinux && echo "+Config.ROOT_PASSWD+" | sudo -S git checkout "+branch+" && git pull origin "+branch)
    #获取文件名
    fileList = exec("ls ~/klinux/arch/"+cpus+"/configs")
    return JsonResponse({"filelist":fileList})


#点击开始编译按钮进行编译
def start_compile(request):
    cpus = request.GET.get("cpus")
    files = str(request.GET.get("file"))
    setting_files = ''
    for file in files.strip().split(' '):
        setting_files+="arch/"+cpus+"/configs/"+file+" "
    command = "cd ~/klinux; echo "+Config.ROOT_PASSWD+" | sudo -S rm -rf build.log ;echo "+Config.ROOT_PASSWD+" | sudo -S nohup ./scripts/buildpackage.sh "+setting_files[:-2]+ " >> build.log & "
    #编译内核
    #os.system(command)
    for command in AfterCompile.commands:
        os.system(command)
    #编译完成之后打包操作
    return JsonResponse({"null":None})

#用于js定时返回日志
def pull_log(request):
    nu = request.GET.get("nu")
    l = exec("cd ~/klinux ; tail -n +"+nu+" build.log ; wc -l build.log")
    nu = l[-1].split(' ')[0]
    log = l[:-1]
    return JsonResponse({"log":log,"nu":int(nu)+1})


#用于下载日志
def download_log(request):
    file=open(exec("cd ~ ; pwd")[0]+"/klinux/build.log","rb")
    response =  HttpResponse(file)
    response["Content-Type"] = 'application/octet-stream'
    response["Content-Disposition"] = 'attachment;filename="build.log"'
    return response


#用于获取内核包的名字
def get_kernel_name(request):
    file_name = exec("cd ~/klinux; ls | grep -E rele*")[0]
    return JsonResponse({"name":file_name})


#用于下载内核
def download_kernel(request):

    pwd = exec("cd /var/data/ftpdata/robot/${DATE}/ ; pwd")[0]
    file_name = exec("cd /var/data/ftpdata/robot/${DATE}/ ; ls | grep -E rele*")[0]
    file = open(pwd+"/"+file_name,"rb")
    response = HttpResponse(file)
    response["Content-Type"] = 'application/octet-stream'
    response["Content-Disposition"] = 'attachment;filename='+file_name+''
    return response


