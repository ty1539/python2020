## 内容回顾

模板

{{  变量  }}      {%  标签  %}

变量

return  render(request,'模板的名字',{'k1':v1})

{{ k1 }}  

.   

.索引    .key   .属性  .方法

优先级

  .key  >    .属性  .方法   >  .索引

过滤器

{{  变量|过滤器 }}  {{   变量|过滤器:参数 }}

add   default   filesizeformat  title lower upper  date  safe  slice  first last length  join  truncatechars truncatewords

标签

for

```
{% for i in list %}
	{{ forloop }}
	{{ i }}
{% endfor %}


{% for i in list %}
	{{ forloop }}
	{{ i }}
	
{% empty %}	
	空
{% endfor %}

```

forloop.counter   当前循环的序号（正序）  从1开始

forloop.counter0   当前循环的序号（正序）  从0开始

forloop.revcounter   当前循环的序号（倒序）  到0结束

forloop.revcounter0  当前循环的序号（倒序）  到1结束

forloop.first  forloop.last   布尔值  判断当前的循环是否是第一次/最后一次的循环 

forloop.parentloop    当前循环的外层循环的参数



if 

```
{% if 条件  %}
	x1
{% elif 条件1  %}	
	x2
{% else %}	
	else
{% enfif %}
```

注意点：

1. 条件中不支持算术运算
2. 不支持连续判断

csrf_token

写在form标签内的，form标签中就多了一个隐藏的input标签，标签的name=‘csrfmiddlewaretoken’，可以提交post请求



母版和继承

母版：

1. 提取多个页面的公共部分放到一个html文件中 （base.html）
2. 在页面中定义block块  

继承：

1. 子页面中写{%  extends  'base.html' %}
2. 重写block块

注意点：

1. {%  extends  'base.html' %} 模板名字外带引号
2. {%  extends  'base.html' %}写在第一行
3. 想要替换的内容要写在block块中
4. 母版中多定义写block块，css/js块



组件

1. 将一小段的HTML文本写入到文件中 （nav.html）
2. 在模板中写{%  include  ‘nav.html’ %}



静态文件

配置

STATIC_URL =  ‘/static/’

STATICFILES_DIRS = [

​	os.path.join(BASE_DIR,'static')

]

引入

```html
<link rel="stylesheet" href="/static/相对路径">
<script src="/static/相对路径"></script>

{% load static %}

<link rel="stylesheet" href="{% static '相对路径' %}">

```



自定义的方法filter、simple_tag、inclusion_tag

1. 在已注册的app下创建一个python包，名字为templatetags 

2. 在包内创建py文件，文件名可自定义（mytags.py）

3. 在py文件中写固定的内容

   ```python
   from django import template
   register = template.Library()  # register 名字不能错 
   ```

4. 写函数 + 加装饰器

   ```python
   @register.filter
   def add_arg(value,arg)
   	return 'xxxx'
   
   @register.simple_tag
   def str_join(*args,**kwargs)：
   	return 'xxxxxx'
   
   @register.inclusion_tag('li.html')
   def show_li(num):
       return {'num':range(1,num+1)}
   
   ```

   li.html

   ```html
   <ul>
   	{% for i in num %}
   		<li> {{i}} </li>
   	{% endfor %}
   </ul>
   
   ```

5. 使用

   ```
   {% load mytags %}
   {{ 'alex'|add_arg:'dsb' }}    'xxxx'
   
   {% str_join 'a' 'b' k1='c' k2='d'  %}   'xxxxxx'
   
   {% show_li 10 %}
   
   ```



## 今日内容

视图

### CBV和FBV

FBV   function based  view

CBV  class based  view

```python
from django.views import View

class Xxx(View):
    
    def get(self,request)
    	# 专门处理get请求
        return response
    
	def post(self,request)
    	# 专门处理post请求
        return response

```

```python
 url(r'xx/',Xxx.as_view())
```

as_view()的流程

1. 项目运行时加载urls.py的文件，执行类.as_view()方法

2. as_view()执行后，内部定义了一个view函数，并且返回。

3. 请求到来的时候，执行view函数：

   1. 实例化类 —— 》 self

   2. self.request  =  request  

   3. 执行self.dispatch(request, *args, **kwargs)的方法

      1. 判断请求方式是否被允许

         1. 允许：

            通过反射获取请求方式对应的请求方法 ——》 handler

            获取不到  self.http_method_not_allowed ——》 handler

         2. 不允许：

            self.http_method_not_allowed ——》 handler

      2. 执行handler，返回结果



```python
from functools import wraps

def timer(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        
        start = time.time()
        ret = func(request, *args, **kwargs)
        print('执行的时间是：{}'.format(time.time() - start))
        return ret

    return inner
```



FBV

直接加在函数上就行

CBV加装饰器：

需要使用一个装饰器

```
from django.utils.decorators import method_decorator
```

1. 加在方法上

   ```python
   @method_decorator(timer)
   def get(self, request):
   ```

2. 加在dispatch方法上

   ```python
   @method_decorator(timer)
   def dispatch(self, request, *args, **kwargs):
       # 之前的操作
       ret = super().dispatch(request, *args, **kwargs)  # 执行View中的dispatch方法
       # 之后的操作
       return ret3
   
   @method_decorator(timer,name='dispatch')
   class PublisherAdd(View):
   ```

3. 加在类上

   ```python
   @method_decorator(timer,name='post')
   @method_decorator(timer,name='get')
   class PublisherAdd(View):
   ```



request 

```python
request.method  请求方法  GET POST 
request.GET    URL上携带的参数   ?k1=v1&k2=v2   { }
request.POST  post请求提交的数据  {}     编码方式是URLencode
request.path_info  路径信息   不包含IP和端口 也不包含参数
request.body  请求体   bytes类型
request.COOKIES   cookie
request.session    session
request.FILES   长传的文件
request.META    头的信息     小写——》大写   HTTP_ 开头   -  ——》 _

request.get_full_path()  完整的路径信息  不包含IP和端口 包含参数
request.is_ajax()    请求是否是ajax请求

```



response

```python
from django.shortcuts import render, HttpResponse, redirect

HttpResponse('字符串')  #   返回字符串
render(request,'模板的文件名'，{'k1':v1})   # 返回一个HTML页面
redirect('地址')  # 重定向  Location：‘地址’  301 302 
```

```
from django.http.response import JsonResponse
JsonResponse({'k1':'v1'})
JsonResponse(data,safe=False)
```







上传文件

urls.py

```
url(r'^upload/', views.Upload.as_view()),
```

视图：

```python
class Upload(View):

    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        file = request.FILES.get('f1')

        with open(file.name, 'wb') as f:
            for i in file:
                f.write(i)

        return HttpResponse('ok')
```

upload.html

```
<form action="" method="post" enctype="multipart/form-data">
    {% csrf_token %}

    <input type="file" name="f1">
    <button>上传</button>
</form>
```





