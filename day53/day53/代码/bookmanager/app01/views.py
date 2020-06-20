from django.shortcuts import render, HttpResponse, redirect, reverse
from app01 import models
from functools import wraps
import time
from django.conf import global_settings

def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        if user == 'alex' and pwd == '123':
            # 登录成功后保存登录状态到cookie中
            url = request.GET.get('url')
            if url:
                return_url = url
            else:
                return_url = reverse('publisher')

            ret = redirect(return_url)
            # ret.set_cookie('is_login', '1')  # 普通cookie
            # ret.set_signed_cookie('is_login', '1', salt='s28',httponly=True)  # 普通cookie
            request.session['is_login'] = 1  # 设置session
            request.session.set_expiry(0)
            return ret
        else:
            error = '用户名或密码错误'
    return render(request, 'login.html', locals())


def logout(request):
    # 清除cookie (某个键值对)
    ret = redirect('/login/')
    # ret.delete_cookie('is_login')
    # del request.session['is_login']
    # request.session.pop('is_login')
    # request.session.delete()
    request.session.flush()

    # 重定向到登录页面
    return ret


def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        print(request.COOKIES)
        # is_login = request.COOKIES.get('is_login')
        # is_login = request.get_signed_cookie('is_login',salt='s28',default='')
        is_login = request.session.get('is_login')
        print(is_login, type(is_login))
        if is_login != 1:
            # 没有登录 跳转到登录页面
            return redirect('/login/?url={}'.format(request.path_info))
        ret = func(request, *args, **kwargs)
        return ret

    return inner


# 统计时间的装饰器
def timer(func):
    def inner(request, *args, **kwargs):
        start = time.time()
        ret = func(request, *args, **kwargs)
        print('执行的时间是：{}'.format(time.time() - start))
        return ret

    return inner


import json
from django.http.response import JsonResponse


def get_json(request):
    data = {'k1': "v1"}
    data = ['1', '2']
    # return HttpResponse(json.dumps({'k1':'v1'}))  # Content-Type: text/html; charset=utf-8
    return JsonResponse(data, safe=False)  # Content-Type: application/json


@login_required
def publisher_list(request):
    # 逻辑
    # 获取所有的出版社的信息
    all_publishers = models.Publisher.objects.all().order_by('id')  # 对象列表
    print(request.session.session_key)
    request.session.clear_expired()
    # print(request.path_info)
    # print(request.body,type(request.body))
    # print(request.scheme,type(request.scheme))
    # print(request.META,type(request.META))
    # print(request.get_full_path())

    return render(request, 'publisher_list.html', {'all_publishers': all_publishers})


# 新增出版社
@login_required
def publisher_add(request):
    if request.method == 'POST':
        # post请求
        # 获取用户提交的数据
        pub_name = request.POST.get('pub_name')
        if not pub_name:
            # 输入为空
            return render(request, 'publisher_add.html', {'error': '出版社名称不能为空'})

        if models.Publisher.objects.filter(name=pub_name):
            # 数据库中有重复的名字
            return render(request, 'publisher_add.html', {'error': '出版社名称已存在'})

        # 将数据新增到数据库中
        ret = models.Publisher.objects.create(name=pub_name)
        print(ret, type(ret))
        # 返回一个重定向到展示出版社的页面
        return redirect(reverse('publisher'))

        # get请求返回一个页面，页面中包含form表单
    return render(request, 'publisher_add.html')


# 新增出版社 CBV
from django.views import View
from django.utils.decorators import method_decorator


# @method_decorator(timer,name='post')
# @method_decorator(timer,name='get')
# @method_decorator(timer, name='dispatch')
class PublisherAdd(View):

    # http_method_names = ['get',]  # 允许提交的请求方式
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        ret = super().dispatch(request, *args, **kwargs)  # 执行View中的dispatch方法
        return ret

    @method_decorator(timer)
    def get(self, request):
        # 处理get请求的逻辑
        print('get')
        print(self.request is request)
        return render(request, 'publisher_add.html')

    def post(self, request):
        # 处理post请求的逻辑
        # post请求
        # 获取用户提交的数据
        print('post')
        print(request.body, type(request.body))

        pub_name = request.POST.get('pub_name')
        if not pub_name:
            # 输入为空
            return render(request, 'publisher_add.html', {'error': '出版社名称不能为空'})

        if models.Publisher.objects.filter(name=pub_name):
            # 数据库中有重复的名字
            return render(request, 'publisher_add.html', {'error': '出版社名称已存在'})

        # 将数据新增到数据库中
        ret = models.Publisher.objects.create(name=pub_name)

        # 返回一个重定向到展示出版社的页面
        return redirect(reverse('publisher'))
        # ret = HttpResponse('', status=301)
        # ret['Location'] = '/publisher_list/'
        # return ret


# 删除出版社
@login_required
def publisher_del(request):
    # 获取要删除数据的id
    pk = request.GET.get('pk')
    print(pk)
    # 根据pk到数据库进行删除
    # models.Publisher.objects.get(pk=pk).delete()  # 查询到一个对象 删除该对象
    models.Publisher.objects.filter(pk=pk).delete()  # 查询到一个对象列表 删除该列表里所有的对象

    # 返回重定向到展示出版社的页面
    return redirect(reverse('publisher'))


# 编辑出版社
def publisher_edit(request, pk):
    # pk = request.GET.get('pk')
    pub_obj = models.Publisher.objects.get(pk=pk)

    if request.method == 'GET':
        # get  返回一个页面 页面包含form表单  input有原始的数据
        return render(request, 'publisher_edit.html', {'pub_obj': pub_obj})
    else:
        # post
        # 获取用户提交的出版社的名称
        pub_name = request.POST.get('pub_name')

        # 修改数据库中对应的数据
        pub_obj.name = pub_name  # 只是在内存中修改了
        pub_obj.save()  # 将修改操作提交的数据库
        # 返回重定向到展示出版社的页面
        return redirect('/publisher/')


# 展示书籍
@login_required
def book_list(request):
    # 查询所有的书籍
    all_books = models.Book.objects.all()  # [ book_obj, ]
    # for book in all_books:
    #     print(book)
    #     print(book.pk)
    #     print(book.name)
    #     print(book.publisher)     # 书籍所关联的出版社对象
    #     print(book.publisher_id)  # 书籍所关联的出版社对象的id

    # 返回一个页面，页面包含书籍数据
    return render(request, 'book_list.html', {'all_books': all_books, 'name': 'publisher_list.html'})


# 新增书籍
def book_add(request):
    error = ''
    if request.method == 'POST':
        # post
        # 获取用户提交数据
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        if not book_name:
            # 用户输入名称为空
            error = '书名不能为空'
        elif models.Book.objects.filter(name=book_name):
            # 名字重复
            error = '书名已存在'
        else:
            # 将数据插入到数据库中
            # models.Book.objects.create(name=book_name, publisher=models.Publisher.objects.get(pk=pub_id))
            models.Book.objects.create(name=book_name, publisher_id=pub_id)
            # 返回重定向到展示书籍页面
            return redirect('/book_list/')
    # 查询所有的出版社
    all_publishers = models.Publisher.objects.all()
    # get 返回一个包含form表单的页面
    return render(request, 'book_add.html', {'all_publishers': all_publishers, 'error': error})


# 删除书籍
def book_del(request):
    # 获取用户提交的要删除数据的id
    pk = request.GET.get('id')
    # 获取要删除的对象，删除
    models.Book.objects.filter(pk=pk).delete()
    # 回复一个重定向到展示页面
    return redirect('/book_list/')


# 编辑书籍
def book_edit(request):
    # 查询要编辑对象的id
    pk = request.GET.get('id')
    # 根据id查到要编辑对象
    book_obj = models.Book.objects.get(pk=pk)

    if request.method == 'POST':
        # post
        # 获取到用户新提交的数据
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        # 编辑的对象做对应的修改
        # 方法一
        # book_obj.name = book_name
        # book_obj.publisher_id = pub_id
        # # book_obj.publisher = models.Publisher.objects.get(pk=pub_id)
        # book_obj.save()  # 保存到数据库
        # 方式二
        models.Book.objects.filter(pk=pk).update(name=book_name, publisher_id=pub_id)

        # 重定向到展示页面
        return redirect('/book_list/')

    # get 请求
    # 返回一个页面 页面包含原始数据

    all_publishers = models.Publisher.objects.all()
    return render(request, 'book_edit.html', {'book_obj': book_obj, 'all_publishers': all_publishers})


# 展示作者
@login_required
def author_list(request):
    # 查询所有的作者
    all_authors = models.Author.objects.all()
    # for author in all_authors:
    #     print(author)
    #     print(author.id)
    #     print(author.name)
    #     print(author.books)  # 关系管理对象
    #     print(author.books.all())  # 所关联的所有的对象
    #     print('*' * 40)

    # 返回一个页面，包含作者的信息
    return render(request, 'author_list.html', {'all_authors': all_authors})


# 新增作者
def author_add(request):
    if request.method == 'POST':
        # post
        # 获取用户提交的数据
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')  # 获取多个数据 list类型
        # print(request.POST)
        # print(author_name)
        # print(book_ids,type(book_ids))
        # 向数据库中插入数据
        # 向作者表插入了作者的信息
        author_obj = models.Author.objects.create(name=author_name)
        # 该作者和提交的书籍绑定多对多的关系
        author_obj.books.set(book_ids)  # 设置多对多关系
        # 返回重定向到展示作者页面
        return redirect('/author_list/')

    # get
    # 查询所有的书籍
    all_books = models.Book.objects.all()
    # 返回一个页面，包含form表单，让用户输入作者姓名，选择作品
    return render(request, 'author_add.html', {'all_books': all_books})


# 删除作者
def author_del(request):
    # 获取要删除对象的id
    pk = request.GET.get('id')
    # 根据id查到对象进行删除
    models.Author.objects.filter(pk=pk).delete()
    # 删除了作者  也删除了和该作者相关的书籍的对应关系  并没有删除书籍的数据
    # 返回重定向到展示作业页面
    return redirect('/author_list/')


# 编辑作者
def author_edit(request):
    # 获取要编辑对象的id
    pk = request.GET.get('id')
    # 根据id获取到作者对象
    author_obj = models.Author.objects.get(pk=pk)

    if request.method == 'POST':
        # post
        # 获取用户提交的数据
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')
        # 给该对象修改数据
        # 修改作者的姓名
        author_obj.name = author_name
        author_obj.save()
        # 修改作者和书的多对多关系
        author_obj.books.set(book_ids)  # 重新设置

        # 返回重定向到展示页面
        return redirect('/author_list/')

    # get

    # 获取所有的书籍
    all_books = models.Book.objects.all()
    # 返回一个页面，页面中包含作者的姓名，包含代表作
    return render(request, 'author_edit.html', {'author_obj': author_obj, 'all_books': all_books})


def delete(request, name, pk):
    # 获取到删除的对象 进行删除
    # dic = {
    #     'publisher': models.Publisher,
    #     'book': models.Book,
    #     'author': models.Author,
    # }
    cls = getattr(models, name.capitalize())
    if not cls:
        return HttpResponse('检测表名')
    ret = cls.objects.filter(pk=pk)
    if ret:
        ret.delete()
    else:
        return HttpResponse('要删除的数据不存在')

    # 返回重定向
    return redirect(name)  # redirect里可以直接写上url的name
