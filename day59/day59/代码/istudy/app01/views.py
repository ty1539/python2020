from django.shortcuts import render, redirect
from app01 import models
import hashlib
from app01.forms import RegForm, ArticleForm, ArticleDetailForm
from utils.pagination import Pagination


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
            request.session['pk'] = user_obj.pk
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
        form_obj = RegForm(request.POST, request.FILES)
        if form_obj.is_valid():
            # 注册成功

            form_obj.save()
            return redirect('login')

    return render(request, 'register.html', {'form_obj': form_obj})


def index(request):
    # 查询所有的文章

    all_article = models.Article.objects.all()
    # print(request.user_obj)
    page = Pagination(request,all_article.count(),5)

    return render(request, 'index.html', {'all_article': all_article[page.start:page.end],'page_html':page.page_html })


def article(request, pk):
    article_obj = models.Article.objects.get(pk=pk)
    return render(request, 'article.html', {'article_obj': article_obj})


def backend(request):
    return render(request, 'dashboard.html')


# 展示文章列表
def article_list(request):
    # 应该是获取当前用户的文章
    all_articles = models.Article.objects.filter(author=request.user_obj)
    page = Pagination(request,all_articles.count(),5)
    return render(request, 'article_list.html', {'all_articles': all_articles[page.start:page.end],'page_html':page.page_html})


# 新增文章
def article_add(request):
    obj = models.Article(author=request.user_obj)
    form_obj = ArticleForm(instance=obj)
    article_detail_form_obj = ArticleDetailForm()

    if request.method == 'POST':
        form_obj = ArticleForm(request.POST, instance=obj)
        article_detail_form_obj = ArticleDetailForm(request.POST)
        if form_obj.is_valid() and article_detail_form_obj.is_valid():
            # #  获取文章详情的字符串
            # detail = request.POST.get('detail')
            # #  创建文章详情的对象
            # detail_obj = models.ArticleDetail.objects.create(content=detail)

            detail_obj = article_detail_form_obj.save()
            form_obj.instance.detail_id = detail_obj.pk
            form_obj.save()  # form_obj.instance.save()
            return redirect('article_list')

    return render(request, 'article_add.html',
                  {'form_obj': form_obj, 'article_detail_form_obj': article_detail_form_obj})


# 编辑文章
def article_edit(request, pk):
    obj = models.Article.objects.filter(pk=pk).first()
    form_obj = ArticleForm(instance=obj)
    article_detail_form_obj = ArticleDetailForm(instance=obj.detail)

    if request.method == 'POST':
        form_obj = ArticleForm(request.POST, instance=obj)
        article_detail_form_obj = ArticleDetailForm(request.POST, instance=obj.detail)

        if form_obj.is_valid() and article_detail_form_obj.is_valid():
            # form_obj.instance.detail.content = request.POST.get('detail')
            # form_obj.instance.detail.save()  # 保存文章详情
            article_detail_form_obj.save()
            form_obj.save()  # 保存文章的信息
            return redirect('article_list')

    return render(request, 'article_edit.html',
                  {'form_obj': form_obj, 'article_detail_form_obj': article_detail_form_obj})


users = [{"name": "alex-{}".format(i), 'pwd': '123'} for i in range(1, 445)]


def user_list(request):
    page = Pagination(request,len(users))
    return render(request, 'user_list.html', {'users': users[page.start:page.end], 'page_html': page.page_html, })
