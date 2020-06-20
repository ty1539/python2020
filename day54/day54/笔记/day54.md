cookie session

cookie是什么？

​		保存在浏览器本地上的一组组键值对

为什么要有cookie？

​		HTTP协议是无状态，每次请求都是相互独立的，没有办法保存状态。

特性：

	1. 由服务让浏览器进行设置 （返回的set-cookie的响应头）

   	2. 浏览将键值对保存在本地（有权利不保存）
      	3. 下次继续时携带对应的cookie（cookie的请求头）

django中操作cookie

```
# 设置cookie
response = HttpReponse('xxx')
response.set_cookie(key,value) # max_age  超时时间  path 生效的路径 
response.set_signed_cookie(key,value,salt='xxx')

# 获取cookie 
request.COOKIES  {}  .get(key)
request.get_signed_cookie(key,salt='xxx',default='')

# 删除cookie   将值设置为空 超时时间设置为0 
response.delete_cookie(key)

```



session

​		保存在服务器上的一组组键值对

为什么要有session？

	1. cookie保存在浏览器本地，不太安全

   	2. cookie的大小和个数受到浏览器的限制

过程：

	1. 第一个请求，没有cookie，设置键值对 ，根据浏览器生成一个唯一标识，给一个字典设置键值对。

   	2. 将字典转成字符串（json序列化），进行加密，将唯一标识和字符串保存在数据库中（django_sessoion）。
      	3. 返回给浏览器唯一标识（sessionid）的cookie
         	4. 下次请求携带sessionid，服务器根据session找到对应的数据（session_data），进行解密，进行反序列化，根据key获取对应的值。

django中操作session

```
# 设置session
reqeust.session[key] = value

# 获取
reqeust.session[key]
reqeust.session.get(key)

# 删除
request.session.pop(key)   del reqeust.session[key] 
request.session.delete()   # 删除所有的键值对   不删除cookie
request.session.flush()    # 删除所有的键值对   也删除cookie

# 其他
默认的超时时间（2周）
request.session.set_expiry(value)     # 设置超时时间
request.session.clear_expired()    # 清除已经失效的session数据


from django.conf import global_settings

SESSION_COOKIE_NAME = 'sessionid' 
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
SESSION_SAVE_EVERY_REQUEST = True  # 每次请求都更新session数据
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # cookie在浏览器关闭时就失效
SESSION_ENGINE = 'django.contrib.sessions.backends.db' # 默认是数据库  文件  缓存  数据库+缓存  加密cookie
```



中间件

django的中间件是全局范围内处理django的请求和响应的框架级别的钩子。

```python 
# 定义
from django.utils.deprecation import MiddlewareMixin

class MD1(MiddlewareMixin):
	def process_request(self,request):
		pass
		
# settings中要注册
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app01.middlewares.my_middleware.MD1',
    'app01.middlewares.my_middleware.MD2',
]

```

5个方法4个特点

### process_request(self,request):

执行时间：

​		路由匹配之前，process_view方法前

参数：

​		request    请求的对象 ，和后续的request都是同一个

执行顺序：

​		按照注册的顺序  顺序 执行 

返回值：

​		None    正常流程 

​		HttpResponse对象  当前中间件之后的中间件中的process_request、路由匹配、process_view、视图都不执行，直接去执行当前中间件的process_response方法



### process_response(self,request,response):

执行时间：

​		视图之后执行

参数：

​		request    请求的对象 ，和后续的request都是同一个

​		response  返回给浏览器的响应对象 

执行顺序：

​		按照注册的顺序  倒序 执行 

返回值：

​		HttpResponse对象  必须返回



### process_view(self,request,view_func,view_args,view_kwargs):

执行时间：

​		路由之后，视图之前执行

参数：

​		request    请求的对象 ，和后续的request都是同一个

​		view_func   视图函数

​		view_args     视图函数所需的位置参数

​		view_kwargs  视图函数所需的关键字参数

执行顺序：

​		按照注册的顺序  顺序 执行 

返回值：

​		None  正常流程

​		HttpResponse对象  当前中间件之后的中间件中的process_view、视图都不执行，直接去执行最后一个中间件的process_response方法

### process_exception(self,request,exception):

执行时间(触发条件)：

​		视图中有异常时才执行

参数：

​		request    请求的对象 ，和后续的request都是同一个

​		exception  异常的对象 

执行顺序：

​		按照注册的顺序  倒序 执行 

返回值：

​		None   当前的中间件没有处理异常，交于下一个中间处理，如果所有的都没有处理，django处理异常

​		HttpResponse对象   当前的中间件处理了异常，后面要执行的process_exception方法就不执行了，执行最后一个中间件的process_response方法



### process_template_response(self,request,response):

执行时间(触发条件)：

​		视图返回TemplateResponse对象

参数：

​		request    请求的对象 ，和后续的request都是同一个

​		response TemplateResponse对象 

执行顺序：

​		按照注册的顺序  倒序 执行 

返回值：

​		HttpResponse对象  必须返回

​		处理对象 

​		response.template_name   模板的名字 

​		response.context_data   模板渲染的变量 {}



JSON 

轻量级的文本数据交换格式

python

支持的数据类型：

​	字符串  数字  布尔值  列表  字典 None 

序列化   

​		python的数据类型 ——》   json字符串

反序列话

​		  json字符串 ——》 python的数据类型



ajax  是一个js的技术，异步发送请求的。

ajax特点：

	1. 异步
 	2. 局部刷新
 	3. 传输的数据量小

简单使用

```js
$.ajax({
    url:'/calc/',
    type:'get',
    data:{
        'x1':$('[name="i1"]').val(),
        'x2':$('[name="i2"]').val(),
    },
    success:function (data) {
        $('[name="i3"]').val(data)
    }
})
```

ajax传收数据：

```js
$.ajax({
    url: '/test/',
    type: 'get',
    data: {
        name: 'alex',
        age: 84,
        hobby: JSON.stringify(['抽烟', '喝酒', '画大饼'])
    },
    success: function (data) {
        console.log(data)
        console.log(data.status)

    }
})
```

使用ajax上传文件

```js
$('#b1').click(function () {

    var formData = new FormData();  // multipart/form-data
    formData.append('name', 'alex');
    formData.append('f1', $('#f1')[0].files[0]);
    {#formData.append('f1',document.getElementById('f1').files[0]);#}

    $.ajax({
        url: '/upload/',
        type: 'post',
        data: formData,
        processData: false, //  ajax不处理数据的编码
        contentType: false, //   不修改content-type的请求头
        success: function (data) {
            alert(data)
        }

    })

})
```



```
from django.views.decorators.csrf import csrf_exempt, csrf_protect，ensure_csrf_cookie
csrf_exempt   加在视图上  该视图不需要进行csrf校验
csrf_protect  加在视图上  该视图需要进行csrf校验
ensure_csrf_cookie  加在视图上  确保返回时设置csrftoken的cookie
```

csrf的校验

```
从cookie中获取csrftoken的值
从request.POST中获取csrfmiddlewaretoken的值或者从请求头中获取x-csrftoken的值
把这两个值做对比，对比成功就接受请求，反之拒绝
```

前提：必须有csrftoken的cookie

1. 使用{% csrf_token %}

2. 使用ensure_csrf_cookie的装饰器，加在视图上

   from django.views.decorators.csrf import  ensure_csrf_cookie



让ajax可以通过django的csrf的校验：

1. 给data添加csrfmiddlewaretoken的键值对
2. 给headers添加x-csrftoken的键值对（导入文件的方式）

最终推荐：导入文件 + 确保有cookie





