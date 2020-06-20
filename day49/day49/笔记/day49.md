## 内容回顾

视图  view

mvc   html

mtv   业务逻辑

FBV  function based view

```python
def xxx(request):
	# 业务逻辑的处理
	
	return response
```

```python
# urls.py
url(r'xxx/',xxx)
```



CBV class based view

```python
from django.views import View
class PublisherAdd(View):
    
    def get(self,request):
        # 处理get请求
        self.request 
        return response
    
    def post(self,request):
        # 处理post请求
        return response
    
```

```python
# urls.py
url(r'publisher_add/',PublisherAdd.as_view())
```

as_view的流程：

1. 程序加载时，执行PublisherAdd.as_view() ——》 view 函数

2. 请求到来的时候执行view函数

   1. view函数中的流程：

      1. 实例化PublisherAdd ——》 self

      2. self.request = request

      3. 执行self.dispatch的方法

         1. 判断请求方式是否被允许

            1. 允许

               通过反射获取请求方式对应请求方法   ——》  handler

               获取不到self.http_method_not_allowed ——》 handler

            2. 不允许

               self.http_method_not_allowed ——》 handler

         2. 执行handler  将方法的结果返回



加装饰器：

FBV  直接加

CBV   

```
from django.utils.decorators import method_decorator
```

```python
1. 加在方法上
@method_decorator(装饰器)
def get(self,request)

2. 加在dispatch方法上
@method_decorator(timer)
def dispatch(self, request, *args, **kwargs):
    ret = super().dispatch(request, *args, **kwargs)  # 执行View中的dispatch方法
    return ret
    
@method_decorator(timer,name='dispatch')
class PublisherAdd(View):    
   
3. 加在类上
@method_decorator(timer,name='post')
@method_decorator(timer,name='get')
class PublisherAdd(View):

```

request

```python
request.method  # 请求方式   GET POST
request.GET    # url上携带的参数  ?k1=v1&k2=v2 {}    ['k1']  .get('k1')
request.POST   # POST请求提交的数据  {}   编码格式是urlencode
request.body   # 请求体  bytes
request.FILES  # 上传的文件
request.META   #  {}  头  HTTP_  小写 ——》 大写  - ——》 _
request.path_info  # 路径信息   不包含IP和端口  也不包含参数
request.COOKIES  # cookie的信息
request.session  # session信息

request.get_full_path()  # 完整的路径 不包含IP和端口  包含参数   ?k1=v1&k2=v2
request.is_ajax()   # 是否是ajax请求
```

response

```python
HttpResponse('字符串')  # 返回字符串 
render(request,'模板的文件名',{})   # 返回一个HTMl页面
redirect('地址')  # 重定向 Location:'地址'  状态码 301 302
JsonResponse({})  # content-type:application/json JsonResponse([],safe=False)
```

上传文件

```
<form action="" method="post" enctype="multipart/form-data" >
	<input type="file" name="ffff">
	<button>上产</button>
</form>
```

```
f1 = request.FILES.get('ffff')
f1.name # 上传文件的名字

for i in f1:
	f.write(i)
```





路由

```python
from django.conf.urls import url

urlpatterns = [
     url(正则表达式, views视图，参数，别名),]
```

正则表达式

```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/$', views.blog),
    url(r'^blog/[0-9]{4}/\d{2}/$', views.blogs),
]

^  以什么开头 
$  以什么结尾
\d 数字
\w 数字字母下划线
{} 
[a-z0-9]
.  匹配换行符之外的标志
+  一个或多个
？  0个或1个
*   0个或多个
```

```python
# 是否开启URL访问地址后面不为/跳转至带有/的路径的配置项
APPEND_SLASH=True
```

分组 

```python
url(r'^blog/([0-9]{4})/\d{2}/$', views.blogs),

url地址上捕获的参数会按照 位置传参 方式传递给视图函数

def blogs(request,year):
```

命名分组

```python
url(r'^blog/(?P<year>[0-9]{4})/(?P<month>\d{2})/$', views.blogs),

url地址上捕获的参数会按照 关键字传参 方式传递给视图函数

def blogs(request,year,month):
```

路由分发

ROOT_URLCONF 

```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app01/', include('app01.urls')),
    url(r'^app02/', include('app02.urls')),

]
```

app01/urls.py

```python
from django.conf.urls import url

from app01 import views

urlpatterns = [

    url(r'^blog/$', views.blog),  # /app01/blog/
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>\d{2})/$', views.blogs,),
]
```

url的命名和反向解析

静态路由

命名：

```python
url(r'^blog/$', views.blog,name='blog'),  # /app01/blog/    ——》 blog
```

反向解析：

模板

```html
{% url  'blog' %}    ——》 /app01/blog/
```

py：

from django.shortcuts import reverse
from django.urls import  reverse

```python
reverse('blog')  # ——》 /app01/blog/
```

#### 分组

```
url(r'^blog/([0-9]{4})/(\d{2})/$', views.blogs,name='blogs'),
```

反向解析：

模板

```
{% url 'blogs' '2020' '02' %}  ——》 /app01/blog/2020/02/
```

py

```
reverse('blogs',args=('2018','08')  ——》 /app01/blog/2018/08/
```

#### 命名分组

```
url(r'^blog/([0-9]{4})/(\d{2})/$', views.blogs,name='blogs'),
```

反向解析：

模板

```
{% url 'blogs' '2020' '02' %}  ——》 /app01/blog/2020/02/
{% url 'blogs'  month='02' year='2020' %}  ——》 /app01/blog/2020/02/
```

py

```
reverse('blogs',args=('2018','08')  ——》 /app01/blog/2018/08/
reverse('blogs',kwargs={'year': '2018', 'month': '12'})  ——》 /app01/blog/2018/12/
```

### namespace

```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app01/', include('app01.urls', namespace='app01')),
    url(r'^app02/', include('app02.urls', namespace='app02')),

]
```

反向解析

```
reverse('namespace:name',args=('2018','08')  ——》 /app01/blog/2018/08/
{% url namespace:name  %}
```







