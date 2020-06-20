from django.shortcuts import render, redirect
from app01 import models
import hashlib
from app01.forms import RegForm, ArticleForm, ArticleDetailForm, CategoryForm, SeriesForm
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

    all_article = models.Article.objects.filter(publish_status=True).order_by('-create_time')
    # print(request.user_obj)
    page = Pagination(request, all_article.count(), 5)

    return render(request, 'index.html', {'all_article': all_article[page.start:page.end], 'page_html': page.page_html})


def article(request, pk):
    article_obj = models.Article.objects.get(pk=pk)
    return render(request, 'article.html', {'article_obj': article_obj})


def backend(request):
    return render(request, 'dashboard.html')


from django.db.models import Q


def get_query(request, field_list):
    # 传入一个列表['title','detail__content'] ,返回一Q对象
    query = request.GET.get('query', '')

    q = Q()
    # Q(Q(title__contains=query)|Q(detail__content__contains=query))
    q.connector = 'OR'
    for field in field_list:
        q.children.append(Q(('{}__contains'.format(field), query)))
    # q.children.append(Q(detail__content__contains=query))

    return q


# 展示文章列表
def article_list(request):
    # 应该是获取当前用户的文章
    from django.http.request import QueryDict

    q = get_query(request, ['title', ])
    all_articles = models.Article.objects.filter(q, author=request.user_obj)
    page = Pagination(request, all_articles.count(), 2)

    return render(request, 'article_list.html',
                  {'all_articles': all_articles[page.start:page.end], 'page_html': page.page_html})


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

            url = request.GET.get('url')
            print(request.GET)
            print(url)
            if url:
                return redirect(url)
            return redirect('article_list')

    return render(request, 'article_edit.html',
                  {'form_obj': form_obj, 'article_detail_form_obj': article_detail_form_obj})


users = [{"name": "alex-{}".format(i), 'pwd': '123'} for i in range(1, 445)]


def user_list(request):
    page = Pagination(request, len(users))
    return render(request, 'user_list.html', {'users': users[page.start:page.end], 'page_html': page.page_html, })


def category_list(request):
    q = get_query(request, ['title', 'pk'])

    all_categories = models.Category.objects.filter(q)  # filter（字段名__contains='xxx'）
    return render(request, 'category_list.html', {'all_categories': all_categories})


def category_add(request):
    form_obj = CategoryForm()

    if request.method == 'POST':
        form_obj = CategoryForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('category_list')

    title = '新增分类'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


def category_edit(request, pk):
    obj = models.Category.objects.filter(pk=pk).first()
    form_obj = CategoryForm(instance=obj)
    if request.method == 'POST':
        form_obj = CategoryForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('category_list')
    title = '编辑分类'

    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


def category_change(request, pk=None):
    obj = models.Category.objects.filter(pk=pk).first()  # pk=None   obj=>None
    form_obj = CategoryForm(instance=obj)
    if request.method == 'POST':
        form_obj = CategoryForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('category_list')

    title = '编辑分类' if pk else '新增分类'

    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


from django.http.response import JsonResponse

from django.utils import timezone


def comment(request):
    obj = models.Comment.objects.create(**request.GET.dict())

    return JsonResponse({'status': True, 'time': timezone.localtime(obj.time).strftime('%Y-%m-%d %H:%M:%S')})


def series_list(request):
    q = get_query(request, [])

    all_series = models.Series.objects.filter(q)  # filter（字段名__contains='xxx'）
    return render(request, 'series_list.html', {'all_series': all_series})


def series_change(request, pk=None):
    obj = models.Series.objects.filter(pk=pk).first()  # pk=None   obj=>None
    form_obj = SeriesForm(instance=obj)
    if request.method == 'POST':
        form_obj = SeriesForm(request.POST, instance=obj)
        if form_obj.is_valid():
            print(form_obj.cleaned_data)
            # form_obj.save()
            # 新增了系列的对象
            form_obj.instance.save()
            obj = form_obj.instance
            # 保存的系列和文章的多对多关系
            obj.articles.set(form_obj.cleaned_data.get('articles'))  # [id ]  [对象]
            # 保存的系列和用户的多对多关系
            users = form_obj.cleaned_data.get('users')
            if not pk:
                obj_list = []
                for user in users:
                    obj_list.append(models.UserSeries(user_id=user.pk, series_id=obj.pk))
                    # models.UserSeries.objects.create(user_id=user.pk,series_id=obj.pk)
                if obj_list:
                    models.UserSeries.objects.bulk_create(obj_list)  # 批量插入
            else:
                # 编辑
                # 新添加用户
                old = set(obj.users.all())
                new = set(users)
                add_users = new - old
                if add_users:
                    obj_list = []
                    for user in add_users:
                        obj_list.append(models.UserSeries(user_id=user.pk, series_id=obj.pk))
                    if obj_list:
                        models.UserSeries.objects.bulk_create(obj_list)  # 批量插入

                # 删除用户
                del_users = old - new
                if del_users:
                    models.UserSeries.objects.filter(series_id=obj.pk, user_id__in=del_users).delete()

            return redirect('series_list')

    title = '编辑系列' if pk else '新增系列'

    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


def profile(request):
    all_user_series = models.UserSeries.objects.filter(user=request.user_obj)
    return render(request, 'profile.html', {'all_user_series': all_user_series})


from django.db.models import F, Sum


def point(request):
    # 插入得分记录
    obj, created = models.PointDetail.objects.get_or_create(**request.GET.dict())

    if created:
        # 更新系列的进度
        query_set = models.UserSeries.objects.filter(user=request.user_obj, series__in=obj.article.series_set.all())
        # 加积分前计算每个系列的总积分

        ret = query_set.values('series_id').annotate(total_points=Sum('series__articles__point'))
        for i in ret:
            models.UserSeries.objects.filter(user=request.user_obj, series_id=i['series_id']).update(
                total_points=i['total_points'])

        # 加积分
        query_set.update(points=F('points') + obj.point, progress=F('points') / F('total_points') * 100)

        return JsonResponse({'status': True})
    return JsonResponse({'status': False})
