from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

'''' 直接跳转到index.html页面 '''
def to_index(request):
    return render(request,"index.html",None)

