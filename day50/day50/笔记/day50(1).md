## 内容回顾

路由

urls.py    urlconf

```python
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index,),  # /app01/blog/    ——》 blog
    url(r'^home/$', views.home, name='home'),  # /app01/blog/    ——》 blog
    url(r'^blog/$', views.blog, name='blog'),  # /app01/blog/    ——》 blog

]
```

正则表达式

^  $   [0-9a-zA-z]{4,6}   \d   \w  +   ?  *  .  

分组和命名分组

分组

```
 url(r'^publisher_edit/(\d+)/$', views.publisher_edit,),
 
 从url上捕获参数按照 位置传参 传递给视图
```

```
 url(r'^publisher_edit/(?P<pk>\d+)/$', views.publisher_edit,),
 
 从url上捕获参数按照 关键字传参 传递给视图
```

include 路由分发

```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app01/', include('app01.urls',)),
    url(r'^app02/', include('app02.urls',)),

]
```

```
urlpatterns = [

    url(r'^index/$', views.index,),  # /app01/blog/    ——》 blog
    url(r'^home/$', views.home,name='home'),  # /app01/blog/    ——》 blog
    url(r'^blog/$', views.blog,name='blog'),  # /app01/blog/    ——》 blog
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>\d{2})/$', views.blogs,name='blogs'),
]
```

url 的命名和反向解析

静态路由

```
url(r'^index/$', views.index,name='index')   # /app01/index/
```

反向解析

模板中：

```
{% url 'index' %}   _> /app01/index/
```

py文件

```
form django.shotcuts import reverse
form django.urls import reverse
reverse('index')    #  ——》 '/app01/index/'
```

动态路由

分组

```
url(r'^publisher_edit/(\d+)/$', views.publisher_edit,name='pub_edit'),
```

反向解析

模板

```
{% url 'pub_edit' pub_obj.pk %}     ——》 /app01/publisher_edit/1/
```

py文件

```
reverse('pub_edit',args=('1',)) #   ——》 /app01/publisher_edit/1/
```

命名分组

```
url(r'^publisher_edit/(?P<pk>\d+)/$', views.publisher_edit,name='pub_edit'),
```

反向解析

模板

```
{% url 'pub_edit' pub_obj.pk %}     ——》 /app01/publisher_edit/1/
{% url 'pub_edit' pk=pub_obj.pk %}     ——》 /app01/publisher_edit/1/
```

py文件

```
reverse('pub_edit',kwargs={'pk':'1'}) #   ——》 /app01/publisher_edit/1/
```

namespace

```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app01/', include('app01.urls',namespace='app01')),
    url(r'^app02/', include('app02.urls',)),

]
```

```
{% url  'app01:index'  %}
reverse('app01:index')

```



常用的字段

```python
AutoField  自增字段 primary_key=True 变成主键
IntegerField    整形  10位  -2147483648 ~ 2147483647。
CharField    字符串   varchar  max_length 必填参数
DateField
DatetimeField   # auto_now_add=True 新增数据时自动保存当前的时间
   				# auto_now=True  新增和编辑数据时自动保存当前的时间
BooleanField  布尔类型
TextField     大文本
FloatField  浮点型
DecimalField  10进制小数   # 999.99
			# max_digits，小数总长度   5
            # decimal_places，小数位长度  2
    

```

自定义一个char类型

```python
class MyCharField(models.Field):
    """
    自定义的char类型的字段类
    """
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(MyCharField, self).__init__(max_length=max_length, *args, **kwargs)
 
    def db_type(self, connection):
        """
        限定生成数据库表的字段类型为char，长度为max_length指定的值
        """
        return 'char(%s)' % self.max_length
```

字段参数

```ptyohn
null=True   该字段在数据库可以为空
blank=True  允许用户输入为空
db_column   数据库中字段的列名
default     默认值
db_index    建立索引
unique      唯一约束
verbose_name 显示的字段名
choices    用户选择的参数
```

表的参数

```python
class Person(models.Model):
    pid = models.AutoField(primary_key=True)  # 主键
    name = models.CharField(verbose_name='姓名', unique=True, db_column='nick',
                            max_length=32, null=True, blank=True)  # varchar(32)
    age = models.IntegerField(default=18)
    phone = MyCharField(max_length=11, unique=True)
    gender = models.BooleanField(choices=((True, 'male'), (False, 'female')))
    birth = models.DateTimeField(auto_now=True)

    # auto_now_add=True 新增数据时自动保存当前的时间
    # auto_now=True  新增和编辑数据时自动保存当前的时间

    def __str__(self):
        return "{}-{}".format(self.name, self.age)

    class Meta:
        # 数据库中生成的表名称 默认 app名称 + 下划线 + 类名
        db_table = "person"

        # admin中显示的表名称
        verbose_name = '个人信息'

        # verbose_name加s
        verbose_name_plural = '所有用户信息'
      
        # 联合索引
        index_together = [
            ("name", "age"),  # 应为两个存在的字段
        ]
        #
        # # 联合唯一索引
        unique_together = (("name", "age"),)  # 应为两个存在的字段
```



使用django的admin：

1. 创建一个超级用户

   python manage.py createsuperuser

2. 在app下的admin.pu中注册model

   ```
   from django.contrib import admin
   from app01 import models
   
   # Register your models here.
   admin.site.register(models.Person)
   ```

3. 登录http://127.0.0.1:8000/admin/操作表

   







