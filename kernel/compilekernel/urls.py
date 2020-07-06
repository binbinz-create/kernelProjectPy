from django.urls import path,include

import compilekernel.views

urlpatterns=[
    path("index",compilekernel.views.to_index),
    path("filelist",compilekernel.views.file_list),
    path("compile",compilekernel.views.start_compile)
]