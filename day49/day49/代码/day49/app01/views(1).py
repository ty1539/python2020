from django.shortcuts import render, HttpResponse, reverse


# Create your views here.
def blog(request):
    url = reverse('app01:blog')  # ——》 /app01/blog/
    print(url, type(url))

    url = reverse('app01:blogs', args=('2018', '08'))  # ——》 /app01/blog/
    url = reverse('app01:blogs', kwargs={'year': '2018', 'month': '12'})  # ——》 /app01/blog/
    print(url, type(url))

    return HttpResponse('app01:blog')


def blogs(request, *args, **kwargs):
    # print(year,type(year))
    # print(month,type(month))
    print(args)
    print(kwargs)
    return HttpResponse('blogs')


def index(request):
    return render(request, 'index.html')


def home(request):
    return HttpResponse('app01 home')
