import os
from django.shortcuts import render
from compilekernel.utils import git_without_passwd
from compilekernel.utils import exec
from compilekernel.utils import client_to_server
from compilekernel.models import Config,AfterCompile
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
#直接跳转到index.html页面
from compilekernel.Dao import Dao


#使用全局变量记录各台机器正在编译的用户,cps架构，分支，版本，配置文件等等
x86_compiling_user=None
arm_compiling_user=None
mips_compiling_user=None
cpus=None
branch=None
version=None
file=None

def to_index(request):
    return render(request, "compilekernel/index.html", None)

def to_login(request):
    return render(request,"compilekernel/login.html",None)

def to_compile(request):
    return render(request,"compilekernel/compiling.html",None)

#直接跳转到test.html页面
def to_test(request):
    return render(request,"compilekernel/test.html",None)

#选择完分之后列出配置文件的请求
def file_list(request):
    cpus = request.GET.get("cpus")
    branch = request.GET.get("branch")
    #免用户名和密码即可操作git
    git_without_passwd("172.16.31.225")
    #切换分支，更新资源
    client_to_server("172.16.31.225","cd ~/klinux && echo "+Config.ROOT_PASSWD+" | sudo -S git checkout "+branch+" && git pull origin "+branch)
    #获取文件名
    fileList = client_to_server("172.16.31.225","ls ~/klinux/arch/"+cpus+"/configs")
    return JsonResponse({"filelist":fileList})

#点击开始编译按钮进行编译
def start_compile(request):
    global compiling_user,branch,version,file,cpus
    cpus = request.GET.get("cpus")
    files = str(request.GET.get("file"))
    #获取配置文件
    setting_files = ''
    for file in files.strip().split(' '):
        setting_files+="arch/"+cpus+"/configs/"+file+" "
    command = "cd ~/klinux; echo "+Config.ROOT_PASSWD+" | rm -rf build.log ;echo "+Config.ROOT_PASSWD+" | sudo -S  ./scripts/buildpackage.sh "+setting_files[:-2]+ " >> build.log"
    #设置正在编译的用户,以及编译的相关信息
    username = request.session.get("user",default=None)
    compiling_user=username
    file = files
    branch = request.GET.get("branch")
    version = request.GET.get("version")
    #进行编译
    os.system(command)
    #编译结束后,将正在编译的用户设置为None
    compiling_user=None
    #判断是否编译成功（有可能编译时，点击了停止编译）
    deb_num = exec("ls ~ | grep -E .*deb | wc -l")
    #~没有*deb文件，则表明没有编译成功
    if(int(deb_num) < 5):
       return JsonResponse({"success":0})
    #编译完成之后打包操作
    os.system("cd ~/klinux ; rm -rf scripts/tar_kernel.sh")
    for command in AfterCompile.commands:
        os.system("echo \""+command+"\" >> ~/klinux/scripts/tar_kernel.sh")
    #run tar_kernel.sh and return such as file path , branch version , architecture, suffix , date
    results =  exec("cd ~/klinux/scripts ; chmod 777 ~/klinux/scripts/tar_kernel.sh ;  ./tar_kernel.sh")
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
                         "suffix":suffix,"branch_version":branch_version,"date":date,"success":1})

#停止编译内核
def stop_compile(request):
    global compiling_user
    list_pid = exec("ps aux | grep build | awk '{print $2}'")
    command = "echo zhubin123 | sudo -S kill -9 "
    compiling_user=None
    for pid in list_pid:
        command += pid + " "
    exec(command)
    return JsonResponse({"stop":1})

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
    #如果不够的话，则返回进程数，查看是否编译过程已经结束
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

#用于判断登录
def login_judge(request):
    dao = Dao()
    username = request.GET.get("username")
    password = request.GET.get("password")
    sql = "select pass_word from tbl_user where user_name = '%s' " % (username)
    results = dao.executeQuerySql(sql);
    if(len(results) == 0):
        return JsonResponse({"success":0})
    password_indb =  results[0][0];
    if(password_indb == password):
        request.session["user"] = username;
        request.session.set_expiry(0)
        return JsonResponse({"success":1})
    else:
        return JsonResponse({"success":0})

#退出登录
def exit_login(request):
    request.session["user"] = None;
    return render(request,"compilekernel/login.html",None)

#返回正在编译的用户，以及正在编译的版本，分支，配置文件等信息
def is_user_compile(request):
    global compiling_user
    return JsonResponse({"compiling_user":compiling_user,"cpus":cpus,"branch":branch,"file":file,"version":version})
