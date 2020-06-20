内容回顾

1. django的命令

 1. 下载安装

    `pip install django==1.11.28 -i 源`

	2. 创建django项目

    `django-admin startproject 项目名称`

	3. 启动项目

    切换到项目的根目录

    `python manage.py runserver`  127.0.0.1:8000

    `python manage.py runserver 80`  127.0.0.1:80

    `python manage.py runserver 0.0.0.0:80`   0.0.0.0:80

	4. 创建app

    `python manage.py startapp app名称`

	5. 数据库迁移的命令

    ```python
    python manage.py makemigrations # 制作迁移文件  检测所有注册的APP下的models的变更，记录下变更记录
    python manage.py migrate # 迁移 将变更记录同步到数据库中
    ```

​	

2.django的配置settings.py

​	BASE_DIR  项目的根目录

​	INSTALLED_APPS = [

​		'app01.apps.App01Config'

]

​	MIDDLEWARE 

​		注释掉一个csrf的中间件，可以提交POST请求

​	TEMPLATES  

​		DIRS  [ os.path.join(BASE_DIR,'tempaltes') ]

​	DATABASES 数据库

​	静态文件

​	STATIC_URL = ‘/static/’  静态文件的别名

​	STATICFILES_DIRS = [

​		 os.path.join(BASE_DIR,'static')

]

3.django项目使用mysql数据库的流程

 1. 手动创建一个mysql数据库

 2. 在settings.py中配置数据库的连接

    ```python
    ENGINE  引擎  mysql
    NAME    数据库的名字
    HOST    数据库的所在的IP
    PORT    3306
    USER    用户名
    PASSWORD  密码
    ```

	3. 告诉django使用pymysql连接mysql数据库

    写在与项目同名的目录下的`__init__.py`中

    ```python
    import pymysql
    pymysql.install_as_MySQLdb()
    ```

	4. 在app下的models.py中写类

    ```python
    class User(models.Model):
    	username = models.CharField(max_length=32) # varchar(32)
    ```

	5. 执行数据库迁移的命令

    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```

4.request

​	request.method  请求方法   GET POST

​	request.GET    URL上携带的参数   ?k1=v1   {}

​	request.POST  post请求提交的数据  {}

5.response

​	HttpResponse('字符串')    返回的是字符串

​	render(request,'模板的名字',{'k1':v1})      返回一个完整的HTML页面

​	redirect('地址')   重定向

6.ORM

​	对象关系映射

​	对应关系

​	类      ——》    表

​	对象  ——》    数据行（记录）

​	属性  ——》    字段

```python
class Publisher(models.Model):
    name = models.CharField(max_length=32)

class Book(models.Model):
    name = models.CharField(max_length=32)
    pub = models.ForeginKey('Publisher',on_delete=models.CASCADE)
    
class Author(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToManyField('Book') # 不创建字段，创建第三张表
    
```

ORM操作：

1.查询

```python
from app01 import models

models.Publisher.objects.all()  # 查询所有的数据 QuerySet  对象列表
models.Publisher.objects.get(name='xx',pk='1')  # 获取有且唯一的一个的对象  
models.Publisher.objects.filter(name='xx',pk='1')  # 获取多个对象  对象列表

pub_obj.pk    pub_obj.name  

book_obj.pub        # 外键  所关联的对象Publisher对象
book_obj.pub_id     # 所关联对象的id

author_obj.books   # 多对多字段   关系管理对象
author_obj.books.all()   # 关联的所有的对象  对象列表

```

2.新增

```python
models.Publisher.objects.create(name='xxx')

models.Book.objects.create(name='xxx',pub=出版社对象)
models.Book.objects.create(name='xxx',pub_id=出版社对象的id)

author_obj = models.Author.objects.create(name='xxx')
author_obj.books.set([1,2])   # 设置多对多关系
```

3.删除

```python
models.Publisher.objects.get(pk=1).delete() # 通过对象进行删除 
models.Publisher.objects.filter(pk=1).delete() # 批量删除
```

4.修改

```python
pub_obj.name = 'xxxx'
pub_obj.save()   # 提交到数据库中保存

models.Publisher.objects.filter(pk=1).update(name='xxxx')
```

7.模板

render(request,'模板的名字',{'k1':v1})   

```html
{{ k1 }}  



{% for i in list  %}
	
	{{ forloop.counter  }}
	{{ i }}

{% endfor %}



{% if 条件 %}
	x1
{% elif 条件1 %}
	x2
{% else %}
	else
{% endif %}
```



MVC:

M：model 模型  操作数据库

V：view  视图    展示数据  HTML

C：controller  控制器 流程 业务逻辑



MTV：

M：model  ORM 

T： template 模板  

V：view  视图   业务逻辑

模板语法

变量  {{  变量 }}

```html
.
.索引  .key  .属性  .方法   方法后不加括号 
优先级：
.key  >  .属性 .方法 >  .索引

```

过滤器：

{{  变量|过滤器:'参数' }}

default：

变量不存在或者为空时使用默认值

add   + 

数字的加法，字符串和列表的拼接

date

```
{{ now|date:'Y-m-d H:i:s' }}
```

settings

```
USE_L10N = False
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_FORMAT = 'H:i:s'
DATE_FORMAT = 'Y-m-d'
```

自定义过滤器

1. 在一个已经注册的app下创建一个名为templatetags的python包 (包的名字不能错)

2. 创建一个python文件，文件名自定义（mytags.py）

3. 在python文件中写：

   ```python
   from django import template
   
   register = template.Library()  # register的名字不能错
   ```

4. 写函数 + 加装饰器

   ```python
   @register.filter
   def add_arg(value, arg):
       # 功能
       return "{}_{}".format(value, arg)
   ```

使用

在模板中：

```html
{% load mytags %}
{{ 'alex'|add_arg:'dsb' }}

```



for

```
<ul>
    {% for name in name_list %}
        <li>{{ forloop.counter }}-{{ name }}</li>
    {% endfor %}

</ul>
```

forloop.counter   当前循环的序号 从1开始

forloop.counter0   当前循环的序号 从0开始

forloop.revcounter   当前循环的序号(倒序) 到1结束

forloop.revcounter0   当前循环的序号(倒序) 到0结束

forloop.first  是否是第一次循环  布尔值

forloop.last  是否是最后一次循环  布尔值

forloop.parentloop   当前循环的外层循环的变量

```
{% for foo in kong %}
    {{ foo }}
{% empty %}
    空空如也
{% endfor %}
```



if

```html
{% if alex.age < 73 %}
    alex正迈向第一个坎

{% elif alex.age == 73 %}
    alex正在第一个坎上

{% elif alex.age < 84 %}
    alex正迈向第二个坎上

{% elif alex.age == 84 %}
    alex正在第二个坎上

{% elif alex.age > 84 %}
    差不多了

{% endif %}
```

注意：

1. 不支持算术运算 
2. 不支持连续判断

```python
{% if 10 > 5 > 1 %}
    正确1
{% else %}
    错误
{% endif %}
```
with

```html
{% with p_list.0.name as alex %}

    {{ alex }}
    {{ alex }}
    {{ alex }}

{% endwith %}

{% with alex=p_list.0.name %}

    {{ alex }}
    {{ alex }}
    {{ alex }}

{% endwith %}
```

csrf_token

```
<form action="" method="post">
    {% csrf_token %}
    <input type="text" name="k1">
    <button>提交</button>
</form>
```

