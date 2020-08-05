from django.urls import path,include

import compilekernel.views

urlpatterns=[
    path("index",compilekernel.views.to_index),
    path("login",compilekernel.views.to_login),
    path("compile_page",compilekernel.views.to_compile),
    path("filelist",compilekernel.views.file_list),
    path("compile",compilekernel.views.start_compile),
    path("pulllog",compilekernel.views.pull_log),
    path("download_log",compilekernel.views.download_log),
    path("test",compilekernel.views.to_test),
    path("get_name",compilekernel.views.get_kernel_name),
    path("download_kernel",compilekernel.views.download_kernel),
    path("stop_compile",compilekernel.views.stop_compile),
    path("login_judge",compilekernel.views.login_judge),
    path("exit_login",compilekernel.views.exit_login),
    path("is_user_compile",compilekernel.views.is_user_compile),
    path("compile_message",compilekernel.views.compile_message),
]