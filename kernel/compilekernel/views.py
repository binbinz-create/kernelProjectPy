from django.shortcuts import render
from compilekernel.utils import git_without_passwd
from compilekernel.utils import exec
from compilekernel.models import Config
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

#直接跳转到index.html页面
def to_index(request):
    return render(request, "compilekernel/index.html", None)

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
    command = "cd ~/klinux; rm -rf build.log; ./scripts/buildpackage.sh "+setting_files + " >> build.log"
    exec(command)


#用于js定时返回日志
def pull_log(request):
    nu = request.GET.get("nu")
    l = exec("cd ~/klinux ; tail +"+nu+" build.log ; wc -l build.log")
    nu = l[-1].split(' ')[0]
    log = l[:-1]
    return JsonResponse({"log":log,"nu":int(nu)+1})
