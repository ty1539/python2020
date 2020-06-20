from django.shortcuts import render, HttpResponse
from django.template.response import TemplateResponse

# Create your views here.
def index(request,*args,**kwargs):
    print('index')
    # print(id(request))
    # print(request.xxx)

    # int('xxxx')
    ret = HttpResponse('index')
    # print('index',id(ret))
    # return render(request,'index.html',{'user':'alex'})
    return TemplateResponse(request,'index.html',{'user':'alex'})
