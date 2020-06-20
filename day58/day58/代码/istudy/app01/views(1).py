from django.shortcuts import render, redirect
from app01 import models
import hashlib
from app01.forms import RegForm, ArticleForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))

        user_obj = models.User.objects.filter(username=username, password=md5.hexdigest(), is_active=True).first()
        if user_obj:
            # 登陆成功
            # 保存登录状态 用户名
            request.session['is_login'] = True
            request.session['username'] = user_obj.username
            url = request.GET.get('url')
            if url:
                return redirect(url)
            return redirect('index')
        error = '用户名或密码错误'
    return render(request, 'login.html', locals())


def logout(request):
    request.session.delete()
    return redirect('index')


def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # 注册成功

            form_obj.save()
            return redirect('login')

    return render(request, 'register.html', {'form_obj': form_obj})


def index(request):
    # 查询所有的文章

    all_article = models.Article.objects.all()
    # is_login = request.session.get('is_login')
    # username = request.session.get('username')
    # print(is_login,username)
    return render(request, 'index.html', {'all_article': all_article})


def article(request, pk):
    article_obj = models.Article.objects.get(pk=pk)
    return render(request, 'article.html', {'article_obj': article_obj})


def backend(request):
    return render(request, 'dashboard.html')


# 展示文章列表
def article_list(request):
    all_articles = models.Article.objects.all()
    return render(request, 'article_list.html', {'all_articles': all_articles})


# 新增文章
def article_add(request):
    form_obj = ArticleForm()
    if request.method == 'POST':
        form_obj = ArticleForm(request.POST)
        if form_obj.is_valid():
            detail = request.POST.get('detail')
            detail_obj = models.ArticleDetail.objects.create(content=detail)
            form_obj.instance.detail_id = detail_obj.pk
            form_obj.save()
            return redirect('article_list')

    return render(request, 'article_add.html', {'form_obj': form_obj})


# 编辑文章
def article_edit(request, pk):
    obj = models.Article.objects.filter(pk=pk).first()
    form_obj = ArticleForm(instance=obj)
    if request.method == 'POST':
        form_obj = ArticleForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.instance.detail.content = request.POST.get('detail')
            form_obj.save()

    return render(request, 'article_edit.html', {'form_obj': form_obj, 'obj': obj})
