'''
登录拦截器
'''
from django.shortcuts import HttpResponseRedirect, render

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path;
        if request.path != '/kernel/login' and request.path != '/kernel/login_judge':
            user = request.session.get('user');
            if user == None:
                return HttpResponseRedirect('/kernel/login')
