from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect,ensure_csrf_cookie


# Create your views here.
@ensure_csrf_cookie
def index(request):
    if request.method == 'POST':
        i1 = request.POST.get('i1')
        i2 = request.POST.get('i2')
        i3 = int(i1) + int(i2)

    return render(request, 'index1.html', locals())


import time


def calc(request):
    x1 = request.POST.get('x1')
    x2 = request.POST.get('x2')
    print(x1)
    print(x2)
    # time.sleep(3)
    x3 = int(x1) + int(x2)

    return HttpResponse(x3)


def calc1(request):
    x1 = request.POST.get('x1')
    x2 = request.POST.get('x2')
    print(x1)
    print(x2)
    x3 = int(x1) + int(x2)

    return HttpResponse(x3)


import json
from django.http.response import JsonResponse


def test(request):
    print(request.POST)
    hobby = json.loads(request.POST.get('hobby'))

    print(hobby, type(hobby))

    return JsonResponse({'status': 200, 'msg': 'ok', 'error': ''})



# @csrf_protect
def upload(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        f1 = request.FILES.get('f1')
        with open(f1.name, 'wb') as f:
            for i in f1:
                f.write(i)

        return HttpResponse('ok')

    return render(request, 'upload.html')
