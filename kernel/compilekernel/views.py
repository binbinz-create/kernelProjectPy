import os
import time
from django.shortcuts import render
from compilekernel.utils import git_without_passwd
from compilekernel.utils import exec
from compilekernel.utils import client_to_server,client_to_server_compile,client_to_server_log
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
x86_compiling_message={}
arm_compiling_message={}
mips_compiling_message={}
#用于在切换到compiling.html时，来判断是否还在编译。（是否正常完成编译，key：username_cpus   value：0代表正在编译，1代表正常完成编译，2代表手动停止编译）
user_compile={}


def to_index(request):
    return render(request, "compilekernel/index.html", None)

def to_login(request):
    return render(request,"compilekernel/login.html",None)

def to_compile(request):
    cpus = request.GET.get("cpus");
    return render(request,"compilekernel/compiling.html",{"cpus":cpus})

#跳转到编译记录的页面
def to_compile_record(request):
    user = request.GET.get("user")
    # Find out all compilation record of the user
    dao = Dao()
    records = dao.executeQuerySql("select * from tbl_record where uid = (select id from tbl_user where user_name=\'"+user+"\') order by date desc;")
    return render(request,"compilekernel/compile_record.html",{"records":records})

def to_compile_record_all(request):
    #Find out all compilation record and render to compile_record_all.html
    dao = Dao()
    records = dao.executeQuerySql("select * from tbl_record order by date desc")
    return render(request,"compilekernel/compile_record_all.html",{"records":records})


#直接跳转到test.html页面
def to_test(request):
    return render(request,"compilekernel/test.html",None)

#选择完分之后列出配置文件的请求
def file_list(request):
    cpus = request.GET.get("cpus")
    branch = request.GET.get("branch")
    IP = None
    ROOT_PASSWD = None
    if cpus == "x86":
        IP=Config.X86_IP
        ROOT_PASSWD=Config.X86_ROOT_PASSWD
    elif cpus == 'arm':
        IP=Config.ARM_IP
        ROOT_PASSWD=Config.ARM_ROOT_PASSWD
    elif cpus == 'mips':
        IP=Config.MIPS_IP
        ROOT_PASSWD=Config.MIPS_ROOT_PASSWD
    #免用户名和密码即可操作git
    git_without_passwd(IP)
    #check if the warehouse exists
    nums = client_to_server(IP,"ls /tmp | grep klinux | wc -l")[0]
    if nums == '0': #if the warehouse does not exist , download the warehouse
        client_to_server(IP,"echo "+ROOT_PASSWD+" | sudo -S git clone http://172.19.140.200/jiangdi/klinux.git /tmp/klinux")
    #切换分支，更新资源
    client_to_server(IP,"cd /tmp/klinux && echo "+ROOT_PASSWD+" | sudo -S git checkout "+branch+" && git pull origin "+branch)
    #获取文件名
    fileList = client_to_server(IP,"ls /tmp/klinux/arch/"+cpus+"/configs")
    return JsonResponse({"filelist":fileList})

#点击开始编译按钮进行编译
def start_compile(request):
    global x86_compiling_message,arm_compiling_message,mips_compiling_message,user_compile
    cpus = request.GET.get("cpus")

    #choose ip and root password according to cpus,set the user being compiled,configuration information , etc.
    username = request.session.get("user",default=None)
    files = str(request.GET.get("file"))
    file = files
    branch = request.GET.get("branch")
    version = request.GET.get("version")
    IP = None
    ROOT_PASSWD=None
    if cpus == "x86":
        IP=Config.X86_IP
        ROOT_PASSWD=Config.X86_ROOT_PASSWD
        x86_compiling_message["cpus"]=cpus
        x86_compiling_message["user"]=username
        x86_compiling_message["branch"]=branch
        x86_compiling_message["version"]=version
        x86_compiling_message["file"] = file
    elif cpus == 'arm':
        IP=Config.ARM_IP
        ROOT_PASSWD=Config.ARM_ROOT_PASSWD
        arm_compiling_message["cpus"]=cpus
        arm_compiling_message["user"]=username
        arm_compiling_message["branch"]=branch
        arm_compiling_message["version"]=version
        arm_compiling_message["file"] = file
    elif cpus == 'mips':
        IP=Config.MIPS_IP
        ROOT_PASSWD=Config.MIPS_ROOT_PASSWD
        mips_compiling_message["cpus"]=cpus
        mips_compiling_message["user"]=username
        mips_compiling_message["branch"]=branch
        mips_compiling_message["version"]=version
        mips_compiling_message["file"] = file
    #获取配置文件
    setting_files = ''
    for file in files.strip().split(' '):
        setting_files+="arch/"+cpus+"/configs/"+file+" "
    command = "cd /tmp/klinux; echo "+ROOT_PASSWD+" | sudo -S rm -rf build.log ; echo "+ROOT_PASSWD+" | sudo -S touch build.log ; echo "+ROOT_PASSWD+" | sudo -S chmod 666 build.log ; echo "+ROOT_PASSWD+" | sudo -S  ./scripts/buildpackage.sh "+setting_files[:-2]+ " >> build.log "
    #进行编译
    user_compile[username+"_"+cpus]=0; #正常编译
#    time.sleep(10)
    client_to_server_compile(IP,command)
    #编译结束后,将正在编译的用户设置为空
    if cpus == "x86":
        x86_compiling_message.clear()
    elif cpus == "arm":
        arm_compiling_message.clear()
    elif cpus == "mips":
        mips_compiling_message.clear()
    #判断是否编译成功（有可能编译时，点击了停止编译）
    deb_num = client_to_server(Config.X86_IP,"ls  /tmp | grep -E .*deb | wc -l")[0]
    #/tmp目录下没有*deb文件，则表明没有编译成功
    if int(deb_num) < 4:
        user_compile[username + "_" + cpus] = 2;
        return JsonResponse({"success":0})
    #编译完成之后打包操作
    client_to_server(IP,"cd /tmp/klinux ; echo "+ROOT_PASSWD+" | sudo -S rm -rf scripts/tar_kernel.sh")
    client_to_server(IP,"cd /tmp/klinux/scripts ; echo "+ROOT_PASSWD+" | sudo -S touch tar_kernel.sh; echo "+ROOT_PASSWD+" | sudo -S chmod 666 tar_kernel.sh")
    for command in AfterCompile.commands:
        client_to_server_compile(IP,"echo "+ROOT_PASSWD+" | sudo -S echo \""+command+"\" >> /tmp/klinux/scripts/tar_kernel.sh")
    #run tar_kernel.sh and return such as file path , branch version , architecture, suffix , date
    results =  client_to_server_compile(IP,"cd /tmp/klinux/ ; echo "+ROOT_PASSWD+" | sudo -S  chmod 777 /tmp/klinux/scripts/tar_kernel.sh ; echo "+ROOT_PASSWD+" | sudo -S ./scripts/tar_kernel.sh")
    file_path = results[-6]
    file_name = results[-6].split('/')[-1]
    kernel_version = results[-5]  #主线版本
    architecture = results[-4]    #应用架构
    suffix = results[-3]          #个性版本
    branch_version = results[-2]  #分支版本
    date = results[-1]            #时间
    #mv build.log to the same directory as kernel
    client_to_server_compile(IP,"echo "+ROOT_PASSWD+" | sudo -S mv /tmp/klinux/build.log /var/data/ftpdata/robot/"+date)
    #The above data will then be stored in the database
    dao = Dao()
    uid = dao.executeQuerySql("select id from tbl_user where user_name = '%s'"% (username))[0][0];
    dao.executeSql("insert into tbl_record (uid,file_path,file_name,kernel_version,architecture,suffix,branch_version,date,ip) "
                   "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (uid,file_path,file_name,kernel_version,architecture,suffix,branch_version,date,IP))
    user_compile[username + "_" + cpus] = 1;  # 将该状态改为正常完成编译
    return JsonResponse({"cpus":cpus,"file_path":file_path,"file_name":file_name,
                         "kernel_version":kernel_version,"architecture":architecture,
                         "suffix":suffix,"branch_version":branch_version,"date":date,"IP":IP,"success":1})

#判断是否有人在编译
def judge_compile(request):
    global x86_compiling_message,arm_compiling_message,mips_compiling_message
    cpus = request.GET.get("cpus");
    if cpus == 'x86' and len(x86_compiling_message) != 0:
        return JsonResponse({"wait": 1, "compiling_message": x86_compiling_message})
    elif cpus == 'arm' and len(arm_compiling_message) != 0:
        return JsonResponse({"wait": 1, "compiling_message": arm_compiling_message})
    elif cpus == 'mips' and len(mips_compiling_message) != 0:
        return JsonResponse({"wait": 1, "compiling_message": mips_compiling_message})
    else:
        return JsonResponse({"wait":0})
#停止编译内核
def stop_compile(request):
    global compiling_user
    cpus = request.GET.get("cpus")
    IP=None
    ROOT_PASSWD=None
    if cpus == 'x86':
        IP=Config.X86_IP
        ROOT_PASSWD=Config.X86_ROOT_PASSWD
        x86_compiling_message.clear()
    elif cpus == 'arm':
        IP=Config.ARM_IP
        ROOT_PASSWD=Config.ARM_ROOT_PASSWD
        arm_compiling_message.clear()
    elif cpus == 'mips':
        IP=Config.MIPS_IP
        ROOT_PASSWD=Config.MIPS_ROOT_PASSWD
        mips_compiling_message.clear()
    list_pid = client_to_server(IP, "ps aux | grep build | awk '$1!~/libvirt+/{print $2}'")
    command = "echo "+ROOT_PASSWD+" | sudo -S kill -9 "
    for pid in list_pid:
        command += pid + " "
    #kill the compiling process
    client_to_server(IP, command)
    #move the build.log to /var/data/ftpdata/robot/
    command="echo "+ROOT_PASSWD+" | sudo -S mv /tmp/klinux/build.log /var/data/ftpdata/robot/"
    client_to_server(IP,command)
    return JsonResponse({"stop":1,"IP":IP})

#用于js定时返回日志
def pull_log(request):
    global user_compile
    nu = int(request.GET.get("nu"))
    cpus = str(request.GET.get("cpus"))
    username=str(request.GET.get("username"));
    IP = None
    if cpus == 'x86':
        IP = Config.X86_IP
    elif cpus == 'arm':
        IP = Config.ARM_IP
    elif cpus == 'mips':
        IP = Config.MIPS_IP
    results = client_to_server(Config.X86_IP,"wc -l /tmp/klinux/build.log")
    build_log_nu=0
    if len(results) > 0:
        build_log_nu = str(results[0]).split(' ')[0]
    else:
        build_log_nu = 0
    #编译进程的数量
    build_process_number = client_to_server_log(IP,"ps aux | grep buildpackage | awk '{print $2}' | wc -l")
    #当前用户是否正常完成编译
    state = 0
    if user_compile.__contains__(str(username+"_"+cpus)):
        state = user_compile[str(username+"_"+cpus)];
    #如果当前build.log的行足够的话,则返回指定的行的日志
    if((nu+20)<int(build_log_nu)):
        log = client_to_server_log(IP,"tail -n 20 /tmp/klinux/build.log")
        return JsonResponse({"log":log,"nu":build_log_nu,"build_process_number":build_process_number,"build_log_nu":build_log_nu})
    #如果正常完成了编译，则返回编译成功后的路径
    elif state==1:
        dao = Dao()
        uid = dao.executeQuerySql("select id from tbl_user where user_name = '%s'" % (username))[0][0]
        message =  dao.executeQuerySql("select * from tbl_record where id = (select max(id) from tbl_record) and uid = '%s' " % (uid))[0]
        return JsonResponse({"cpus":cpus,"IP":IP,"message":message,"build_process_number": build_process_number, "nu": nu, "build_log_nu": build_log_nu})
    #如果编译失败，则返回编译失败的信息
    elif state==2:
        return JsonResponse({"IP":IP,"fail":1})
    #如果不够的话，则返回进程数，查看是否编译过程已经结束
    else:
        nu = int(build_log_nu) if nu > int(build_log_nu) else nu
        return JsonResponse({"build_process_number":build_process_number,"nu":nu,"build_log_nu":build_log_nu})

#用于获取内核包的名字
def get_kernel_name(request):
    file_name = exec("cd ~/klinux; ls | grep -E rele*")[0]
    return JsonResponse({"name":file_name})

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

#返回三台机器正在编译的用户
def is_user_compile(request):
    global x86_compiling_message,arm_compiling_message,mips_compiling_message
    return JsonResponse({"x86_compiling_message":x86_compiling_message,"arm_compiling_message":arm_compiling_message,"mips_compiling_message":mips_compiling_message})

#返回正在编译的相关信息
def compile_message(request):
    cpus = request.GET.get("cpus")
    #select specified compiling message based on cpus
    compiling_message=None
    if cpus == 'x86':
        compiling_message=x86_compiling_message
    elif cpus == 'arm':
        compiling_message=arm_compiling_message
    elif cpus == 'mips':
        compiling_message=mips_compiling_message
    return JsonResponse({"compiling_message":compiling_message})

#return the current state of user , such as compile , queue and others
def user_state(request):
    user_name = request.GET.get("username")
    #The cpus that current user is compiling
    compile_cpus = []
    if len(x86_compiling_message)!=0 and x86_compiling_message["user"] == user_name:
        compile_cpus.append("x86")
    if len(arm_compiling_message)!=0 and arm_compiling_message["user"] == user_name:
        compile_cpus.append("arm")
    if len(mips_compiling_message)!=0 and mips_compiling_message["user"] == user_name:
        compile_cpus.append("mips")
    return JsonResponse({"compile_cpus":compile_cpus})
