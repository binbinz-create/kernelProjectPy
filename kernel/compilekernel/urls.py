from django.urls import path,include

import compilekernel.views

urlpatterns=[
    path("index",compilekernel.views.to_index)
]