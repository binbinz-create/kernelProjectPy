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
    #获取配置文件
    setting_files = ''
    for file in files.strip().split(' '):
        setting_files+="arch/"+cpus+"/configs/"+file+" "
    command = "cd ~/klinux; echo "+Config.ROOT_PASSWD+" | rm -rf build.log ;echo "+Config.ROOT_PASSWD+" | sudo -S  ./scripts/buildpackage.sh "+setting_files[:-2]+ " >> build.log  "
    #编译内核
    os.system(command)
    #编译完成之后打包操作
    os.system("cd ~/klinux ; rm -rf tar_kernel.sh")
    for command in AfterCompile.commands:
        os.system("echo \""+command+"\" >> ~/klinux/tar_kernel.sh")
    #run tar_kernel.sh and return such as file path , branch version , architecture, suffix , date
    results =  exec("cd ~/klinux ; chmod 777 ~/klinux/tar_kernel.sh ;  ./tar_kernel.sh")
    file_path = results[-6]
    file_name = results[-6].split('/')[-1]
    kernel_version = results[-5]  #主线版本
    architecture = results[-4]    #应用架构
    suffix = results[-3]          #个性版本
    branch_version = results[-2]  #分支版本
    date = results[-1]            #时间
    #The above data will then be stored in the database
    return JsonResponse({"file_path":file_path,"file_name":file_name,
                         "kernel_version":kernel_version,"architecture":architecture,
                         "suffix":suffix,"branch_version":branch_version,"date":date})

#停止编译内核
def stop_compile(request):
    list_pid = exec("ps aux | grep build | awk '{print $2}'")
    command = "echo zhubin123 | sudo -S kill -9 "
    for pid in list_pid:
        command += pid + " "
    exec(command)
    return None

#用于js定时返回日志
def pull_log(request):
    nu = int(request.GET.get("nu"))
    build_log_nu = str(exec("wc -l ~/klinux/build.log")[0]).split(' ')[0]
    #编译进程的数量
    build_process_number = exec("ps aux | grep buildpackage | awk '{print $2}' | wc -l")
    #如果当前build.log的行足够的话,则返回十行日志
    if((nu+20)<int(build_log_nu)):
        log = exec("sed -n '"+str(nu)+","+str((nu+20))+"p' ~/klinux/build.log")
        return JsonResponse({"log":log,"nu":(nu+20),"build_process_number":build_process_number,"build_log_nu":build_log_nu})
    else:
        return JsonResponse({"build_process_number":build_process_number,"nu":nu,"build_log_nu":build_log_nu})

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
    file_path = request.GET.get("file_path")
    file = open(file_path,"rb")
    response = HttpResponse(file)
    response["Content-Type"] = 'application/octet-stream'
    response["Content-Disposition"] = 'attachment;filename='+str(file_path).split('/')[-1]+''
    return response
