## 内容回顾

{{ }}   变量

{%  %}  标签 

.

{{  变量.索引 }}

{{  变量.key }}

{{  变量.属性 }}

{{  变量.方法 }}

优先级：

.key   >  .属性和方法  > .索引

过滤器

{{  变量|filter }}   {{  变量|filter:参数 }}

内置的过滤器

default    给变量加默认值  

add  +    数字的加法  字符串的拼接  列表的拼接

safe 告诉django前面的字符串不需要做转义

upper   lower  title  

filesizeformat  文件的大小显示成带单位的

slice     切片  {{  list|slice:'::' }}

length   返回变量的长度

truncatechars   根据字符的长度进行截断 

truncatewords   根据单词的长度进行截断 

join     字符串的拼接

date   日期时间的格式化  ‘Y-m-d H:i:s’

​	TIME_ZONE = 'Asia/Shanghai'

​	USE_L10N = False  

​	DATETIME_FORMAT =  ‘Y-m-d H:i:s’

​	DATE_FORMAT =  ‘Y-m-d’

​	TIME_FORMAT =  ‘H:i:s’



自定义过滤器

1. 在已经注册的app下创建一个python包，包的名字为templatetags;

2. 在python包中创建py文件，文件可自定义（mytags.py）

3. 在py文件中写代码：

   ```python
   from django import template
   
   register = template.Library()
   
   ```

4. 写函数  + 加装饰器

   ```python
   @register.filter
   def add_arg(value,arg):
   	return  'xxxx'
   
   ```

使用：

```html
{% load mytags %}

{{ 'xx'|add_arg:'xxx' }}


```

标签 tag

for

```
{% for i in list %}

	{{ forloop }}
	{{ i }}
	
{% endfor %}
```

forloop.counter   当前循环的正序的序号   从1开始

forloop.counter0   当前循环的正序的序号   从0开始

forloop.revcounter   当前循环的倒序的序号   到1结束

forloop.revcounter0   当前循环的倒序的序号   到0结束

forloop.first    当前的循环是否是第一次循环   布尔值

forloop.last    当前的循环是否是最后一次循环   布尔值

forloop.parentloop  当前循环的外层循环的相关参数

if

```html
{%  if 条件 %}
	x1
{%  elif 条件1 %}
	x2
{%  else %}
	slse
{%  endif %}
```

注意点：

1. 条件中不能写 算术运算
2. 不支持连续判断



with 

```

{% with alex.name as alex  %}
	{{ alex }}
{% endwith %}


{% with alex = alex.name  %}
	{{ alex }}
{% endwith %}

```

csrf_token

{% csrf_token %}写在form标签中，form标签中就有一个隐藏的input标签，name='csrfmiddlewaretoken'

```
{% widthratio 100 2 1 %}
{#  a b c   a/b*c  #}
```



mark_safe

```python
from django.utils.safestring import mark_safe


@register.filter
def show_a(name, url):
    return mark_safe('<a href="http://{}">{}</a>'.format(url, name))
```





母版和继承

母版：

1. 一个包含多个页面的公共部分  
2. 定义多个block块，让子页面进行覆盖

继承：

	1. {% extends  '母版的名字' %}
 	2. 重新复写block块

注意点:

1. {% extends  '母版的名字' %}  母版的名字带引号

2. {% extends  '母版的名字' %}写在第一行，上面不再写内容
3. 要显示的内容要写在block块中
4. 多写一个css\js的block块

组件

1. 把一小段公用的HTML文本写入一个HTML文件  ， nav.html

2. 在需要该组件的模板中

   ```html
   {% include 'nav.html' %}
   ```



静态文件相关：

```html
{% load static %}

<link rel="stylesheet" href="{% static 'plugins/bootstrap-3.3.7-dist/css/bootstrap.min.css' %}">
<link rel="stylesheet" href="{% static 'css/dsb.css' %}">
```

filter 



filter、simple_tag、inclusion_tag

1. 在已经注册的app下创建一个python包，包的名字为templatetags;

2. 在python包中创建py文件，文件可自定义（mytags.py）

3. 在py文件中写代码：

   ```python
   from django import template
   
   register = template.Library()
   
   ```

4. 写函数  + 加装饰器

   ```python
   @register.filter
   def add_arg(value,arg):
   	return  'xxxx'
   
   @register.simple_tag
   def str_join(*args, **kwargs):
       return "{}_{}".format('_'.join(args), '*'.join(kwargs.values()))
   
   
   @register.inclusion_tag('page.html')
   def pagination(num):
       return {'num': range(1, num + 1)}
   
   ```
   
   page.html
   
   ```html
   <nav aria-label="Page navigation">
       <ul class="pagination">
           <li>
               <a href="#" aria-label="Previous">
                   <span aria-hidden="true">&laquo;</span>
               </a>
           </li>
           {% for li in num %}
               <li><a href="#">{{ li }}</a></li>
           {% endfor %}
   
           <li>
               <a href="#" aria-label="Next">
                   <span aria-hidden="true">&raquo;</span>
               </a>
           </li>
       </ul>
   </nav>
   ```
   
5. 使用

   ```html
   {% load mytags %}
   
   {{ 'alex'|add_arg:'dsb' }}
   
   {% str_join 'a' 'b' 'c' k1='d' k2='e' k3='f' %}
   
   {% pagination 10 %}
   
   ```

   











