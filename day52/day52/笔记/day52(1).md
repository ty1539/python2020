## 内容回顾

单表的双下划线

```python
models.Person.objects.filter(id__gt=4)  # 大于  greater than 
models.Person.objects.filter(id__lt=4)  # 小于   less than 
models.Person.objects.filter(id__gte=4)  # 大于等于   greater than equal
models.Person.objects.filter(id__lte=4)  # 小于等于   less than equal

models.Person.objects.filter(id__range=[1,5])  # 范围 左右都包含 
models.Person.objects.filter(id__in=[1,5])  # 成员判断

models.Person.objects.filter(name__contains='alex')   # like 
models.Person.objects.filter(name__icontains='alex')   # like  忽略大小写

models.Person.objects.filter(name__startswith='alex')   # 以什么开头 
models.Person.objects.filter(name__istartswith='alex')   # 以什么开头  忽略大小写

models.Person.objects.filter(name__endswith='alex')   # 以什么结尾  
models.Person.objects.filter(name__iendswith='alex')   # 以什么结尾  忽略大小写

models.Person.objects.filter(birth__year='2020') 
models.Person.objects.filter(birth__contains='2020-02') 

models.Person.objects.filter(name__isnull=True)   # 字段是否为null
```

外键的操作

```PYTHON
class Publisher(models.Model):
	name = models.CharField(max_length=32)


class Book(models.Model):
	name = models.CharField(max_length=32)
	pub = models.ForeginKey('Publisher',on_delete=models.CASCADE,related_name='books')  # pub_id
```

```python
#  基于对象的查询
book_obj = Book.objects.get(pk=1)
# 正向查询
book_obj.pub      # 所关联的对象    
book_obj.pub_id   # 所关联的对象的id
# 反向查询
pub_obj = Publisher.objects.get(pk=1)

# 不指定related_name  使用 类名小写_set
pub_obj.book_set  # 关系管理对象
pub_obj.book_set.all()  # 所关联的所有的书籍对象

# 指定related_name='books'
pub_obj.books.all()

# 基于字段的查询
ret = Book.objects.filter(name='xxxx')
ret = Book.objects.filter(pub__name='出版社')

ret = Publisher.objects.filter(name='出版社')

# 不指定related_name
ret = Publisher.objects.filter(book__name='xxx')
# 指定related_name='books'
ret = Publisher.objects.filter(books__name='xxx')
# 指定related_query_name='xxx'
ret = Publisher.objects.filter(xxx__name='xxx')

```

多对多的操作

```python
class Book(models.Model):
	name = models.CharField(max_length=32)
	pub = models.ForeginKey('Publisher',on_delete=models.CASCADE,related_name='books')  # pub_id

class Author(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToMantField('Book')

author_obj.books  # 管理管理对象
# all  查询所有关联的对象
author_obj.books.all()  

# set  设置关系   [1,2]    [对象，对象]
author_obj.books.set([1,2])  # []

# add  新增关系    id   对象
author_obj.books.add(1,2) 

# remove  删除关系    id   对象
author_obj.books.remove(1,2) 

# clear  清空关系
author_obj.books.clear() 

# create  新增一个所关联的对象，并且和当前的对象绑定关系
author_obj.books.create(name='xxx',pub_id='1')


# 一对多关系中 反向查询获取到的关系管理对象  
# 参数中只能使用对象，不能使用id 
# 当ForeginKey中有参数null=True时，才有remove、clear方法
    
```

## 今日内容

聚合和分组

```python
from django.db.models import Max, Min, Count, Sum, Avg

# 聚合 aggregate  终止子句
ret = models.Book.objects.filter(id__gt=2).aggregate(min=Min('price'),max=Max('price')) 

#  分组   group by
# annotate  注释   过程中使用了分组
# 1. 统计每一本书的作者个数
ret = models.Book.objects.annotate(Count('authors')).values()  # 添加额外的信息

# 2. 统计出每个出版社卖的最便宜的书的价格
# 方法一
ret = models.Publisher.objects.annotate(Min('book__price')).values()

# 方法二
########## 错误写法 ##########
# ret = models.Book.objects.annotate(Min('price')).values()  按照书分组
########## 正确写法 ##########
# 按照 pub_id  pub__name 分组
ret = models.Book.objects.values('pub','pub__name').annotate(min=Min('price'))

# 3. 统计不止一个作者的图书
ret = models.Book.objects.annotate(count=Count('authors')).filter(count__gt=1)

# 4. 根据一本图书作者数量的多少对查询集 QuerySet进行排序
ret = models.Book.objects.annotate(count=Count('authors')).order_by('-count')

# 5.查询各个作者出的书的总价格
ret = models.Author.objects.annotate(sum=Sum('books__price')).values()
ret = models.Book.objects.values('authors','authors__name').annotate(sum=Sum('price'))

```

F和Q

```python
from django.db.models import F, Q

ret = models.Book.objects.filter(kucun__lt=50)

ret = models.Book.objects.filter(sale__gt=F('kucun'))  # where  'sale' > 'kucun'

# ret = models.Book.objects.filter(id__lte=3).update(sale=F('sale') * 2 + 13)

# Q()
# |   或
# &   与
# ~   非

ret = models.Book.objects.filter(Q(id__lt=3) | Q(id__gt=5))

ret = models.Book.objects.filter(Q(Q(id__lt=3) | Q(id__gt=5))&Q(name__startswith='天然'))

ret = models.Book.objects.filter(Q(Q(id__lt=3) | Q(id__gt=5))&~Q(name__startswith='天然'))
```

事务

```python
from app01 import models
from django.db.models import F
from django.db import transaction

try:
    with transaction.atomic():
        # 一系列的操作
        models.Book.objects.all().update(kucun=F('kucun') - 10)
        models.Book.objects.all().update(sale=F('sale') + 10)
except Exception as e:
    print(e)
```



cookie 

保存在浏览本地上的一组组键值对

特性：

1. 由服务器让浏览器进行设置的
2. cookie信息保存在浏览器本地的，可以浏览器有权不保存
3. 浏览器再次访问时自动携带对应的cookie

django中操作cookie

```python
# 设置cookie：
response.set_cookie(key,value)  # Set-Cookie: is_login=1
response.set_signed_cookie('key', value, salt='s28')  # 加密cookie
设置cookie的参数
# max_age  超时时间
# path  cookie生效的路径
# secure=True  https进行传输
# httponly=True   只能传输，无法被JavaScript获取

# 获取cookie 
request.COOKIES  {}    #  请求头 Cookie: is_login=1;
request.get_signed_cookie('key', salt='s28',defalut='')  # 加密cookie

# 删除cookie   设置cookie 值为空  超时时间为0
response.delete_cookie(key)

```

