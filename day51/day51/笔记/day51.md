## 内容回顾

ORM 

对应关系

类     ——》    表

对象  ——》   数据行（记录）

属性  ——》  字段

django使用mysql数据库的流程：

1. 创建一个mysql数据库

2. 在settings中配置数据库

   ```
   ENGINE  mysql
   NAME  数据库的名称
   HOST  127.0.0.1
   PORT  端口 3306 
   USER  用户名
   PASSWORD 密码
   ```

3. 告诉django使用pymysql模块连接mysql数据库

   ```
   # 写在与项目同名的目录下的__init__.py中
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

4. 在app下的models.py中写类

   ```python
   from  django.db import models
   class Person(models.Model)：
   	name = models.CharField(max_length=32)  # varchar(32)
   
   ```

5. 执行数据库迁移的命名

   ```python
   python manage.py  makemigrations  
   python manage.py  migrate  #  --fake
   ```

常用的字段

```
AutoField    自增字段  primary_key=True
CharField    字符串  max_length必填
BooleanField  布尔类型
IntegerField  整形  -21亿  —— +21亿  10位
DateField 
DateTimeField  auto_now = True  新增和编辑时保存当前的时间
			   auto_now_add = True  新增时保存当前的时间
TextField   文本类型
```

字段的参数

```
null     数据库可以为空
blank    用户输入可以为空
unique   唯一约束
verbose_name  提示信息
choices    让用户选择的数据  choices=( (1,'男')，(2,'女') )
default  默认值
db_column  列名
```

必知必会13条

```python
返回对象列表  
all     查询所有的数据
filter   查询所有满足条件的数据
exclude  查询所有不满足条件的数据
values     查询数据的字段和值   [ {}]
values_list   查询数据的值  [ () ]
order_by   排序  默认升序 -  多字段排序 age id 
reverse   对已经排好序的queryset翻转
distinct  去重

返回对象
get   获取有且唯一的对象
first 
last 

返回布尔值
exists   

数字 
count  
```

路由 

```
url(r'^publisher_list/$',views.publisher_list)
url(r'^(publisher|book|author)_del/$',views.delete)

\d  \w  .  +  ?  *

r'^app01/publisher_list/$'


```



URL的命名和反向解析 

```
url(r'^publisher_list/$',views.publisher_list,name='pub')
```

模板

```
{%  url  'pub' %}   '/publisher_list/'
```

py文件

```
from django.shotcuts import reverse
reverse('pub')   '/publisher_list/'
```

动态路由

分组

```
url(r'^publisher_deit/(\d+)/$',views.publisher_list,name='pub_edit')
```

模板

```
{%  url 'pub_edit' 5  %}   '/publisher_deit/5/'
```

py文件

```
from django.shotcuts import reverse
reverse('pub_edit',args=(5,))   '/publisher_deit/5/'
```

命名分组

```
url(r'^publisher_deit/(?P<pk>\d+)/$',views.publisher_list,name='pub_edit')
```

模板

```
{%  url 'pub_edit' 5  %}   '/publisher_deit/5/'
{%  url 'pub_edit' pk=5  %}   '/publisher_deit/5/'
```

py文件

```
from django.shotcuts import reverse
reverse('pub_edit',args=(5,))   '/publisher_deit/5/'
reverse('pub_edit',kwargs={'pk':'6'}   '/publisher_deit/6/'
```



今日内容

单表的双下划线

```python
ret = models.Person.objects.filter(pid__lt=6)  # 字段__条件 =    less than 小于
ret = models.Person.objects.filter(pid__gt=6)  # 字段__条件 =    greater than 大于
ret = models.Person.objects.filter(pid__lte=6)  # 字段__条件 =   less than equal 小于等于
ret = models.Person.objects.filter(pid__gte=6)  # 字段__条件 =   greater than equal 大于等于

ret = models.Person.objects.filter(pid__range=[1,6])    # 范围
ret = models.Person.objects.filter(pid__in=[1,5,6])     # 成员判断

ret = models.Person.objects.filter(name__contains='alex')   # like
ret = models.Person.objects.filter(name__icontains='alex')  # like ignore忽略   忽略大小写

ret = models.Person.objects.filter(name__startswith='aaa')  # 以什么开头
ret = models.Person.objects.filter(name__istartswith='aaa') # 以什么开头 忽略大小写

ret = models.Person.objects.filter(name__endswith='aaa')   # 以什么结尾
ret = models.Person.objects.filter(name__iendswith='aaa')  # 以什么结尾 忽略大小写

ret = models.Person.objects.filter(birth__year='2019')
ret = models.Person.objects.filter(birth__contains='-01-')

ret = models.Person.objects.filter(name__isnull=True)   # 是否为null
```



外键的操作

```python
################### 基于对象的查询 ####################

# 正向查询
book_obj = models.Book.objects.get(pk=1)
# print(book_obj.pub)  # 关联的出版社对象
# print(book_obj.pub_id)  # 关联的出版社的id

# 反向查询
pub_obj = models.Publisher.objects.get(pk=1)
# 没有指定related_name  类名小写_set
# print(pub_obj)
# print(pub_obj.book_set,type(pub_obj.book_set))   # 类名小写_set   关系管理对象
# print(pub_obj.book_set.all())

# 指定related_name='books'  没有 类名小写_set 的写法



################### 基于字段的查询 ####################
ret = models.Book.objects.filter(pub__name='新华出版社')

# 不指定related_name='books'    类名小写
# ret = models.Publisher.objects.filter(book__name='坐在床上学xx')

# 指定related_name='books'  不指定related_query_name
# ret = models.Publisher.objects.filter(books__name='坐在床上学xx')

# 指定related_query_name='book'
# ret = models.Publisher.objects.filter(book__name='坐在床上学xx')
```

多对多的操作

```python
author_obj = models.Author.objects.get(pk=1)


# 关系管理对象的方法
# all  查询所有的对象

# set 设置多对多的关系  [id,id]  [对象，对象]
# author_obj.books.set([1,2])
# author_obj.books.set(models.Book.objects.filter(id__in=[3, 4]))

# add  添加多对多关系  id或者对象
# author_obj.books.add(1, 2)
# author_obj.books.add(*models.Book.objects.filter(id__in=[5, 6]))

# remove  删除多对多关系  id或者对象
# author_obj.books.remove(1, 2)
# author_obj.books.remove(*models.Book.objects.filter(id__in=[5, 6]))

# clear   清空多对多关系
# author_obj.books.clear()

# create  新建一个对象和当前的对象建立关系
# author_obj.books.create(name='天然懵逼了没',pub_id=1)
ret = book_obj.authors.create(name='天然')

###################  外键  ###################

# set  add  create   参数只能写对象 不能写id
# pub_obj.books.set(models.Book.objects.filter(id__in=[1,2,3,4] ))
pub_obj.books.add(*models.Book.objects.all())

# remove clear  外键字段参数 null=True 才有这两个方法
# pub_obj.books.clear()

```