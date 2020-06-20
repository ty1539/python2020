## 内容回顾

发请求的途径：

1. 直接在地址栏输入地址  get 
2. form表单提交    method=‘post’     get/post
3. a标签    get 
4. ajax

ajax

使用js的技术与服务进行异步交互。

特点：

1. 异步
2. 局部刷新
3. 传输的数据量小

使用：

```js
导入jquery.js

<script>
	var v1 = 'v1'
	$.ajax({
		url:'地址',
		type:'post'， // 请求方式
        headers:{
        	x-csrftoken:'asdasdkljlqjklqewqweweqwe'
    },
		data:{
			k1: v1,
            k2:'v2',
        	// csrfmiddlewaretoken:'xasdaskklqjwkleqweqweqweqweqwe'
        
		},
		success:function(data) {  // data 是返回响应的响应体 
			//  后续的操作	
		
		}
	
	})

</script>
```

上传文件

```
html

<input type='file'  id='f1'>
<button id='b1' >上传</button>


<script>
	
	$('#b1').click(function(){
		
		var formData = new FormData()
		formData.append('csrfmiddlewaretoken','sasdqljqweqwljeljqjlqwjewe')
		formData.append('xxx',$('#f1')[0].files[0])
	
		$.ajax({
            url:'地址',
            type:'post'， // 请求方式
            processData:false,   //   不需要处理编码 formdata
            contentType:false,	 //  不处理content-type 的请求头
            data:formData,
            success:function(data) {  // data 是返回响应的响应体 
                //  后续的操作	
		
		}
	
	})
	
	})

</script>

```

前提条件：必须确保有csrftoken的cookie

1. 使用{%  csrf_token %}标签
2. 给视图加上ensure_csrf_cookie装饰器



ajax通过django的csrf的校验：

1. 给data中添加csrfmiddlewaretoken的键值对
2. 给headers中添加x-csrftoken的请求头

推荐的方式：导入文件  + 使用{%  csrf_token %}





csrf的中间件的流程：

1. process_request

   从cookie中获取了csrftoken的值，将该值放入request.META中

2. process_view

   1. 判断视图是否使用了csrf_exempt的装饰器，使用了就不再进行csrf 的校验了

   2. 判断请求方式是否是get head potions trace：

      1. 如果是   直接接受该请求  不做csrf的校验

      2. 不是 这些请求 要进行csrf的校验：

         1. csrf_token = request.META.get('CSRF_COOKIE') # cookie中csrftoken的值

         2. request_csrf_token  = ‘’

         3. 请求方式是post，尝试从request.POST中获取csrfmiddlewaretoken的值

            ```
            request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
            ```

         4. 如果request_csrf_token  = ‘’，再尝试从请求头中获取X-CSRFTOKEN的值

            ```
            request_csrf_token = request.META.get(settings.CSRF_HEADER_NAME, '')
            ```

         5. 比较csrf_token和request_csrf_token

            1. 比较成功 通过校验
            2. 比较不成功 拒绝请求



form组件定义



```
class RegForm(forms.Form):
    user = forms.CharField(label='用户名')
    pwd = forms.CharField(label='密码')
```

使用：

```python
def reg2(request):
    form_obj = RegForm()  # 空的form
    if request.method == 'POST':
        # 对提交的数据做校验
        form_obj = RegForm(request.POST)  # 包含用户提交的数据的form
        if form_obj.is_valid():  # 对数据进行校验
            # 校验成功
            return HttpResponse('注册成功')

    return render(request, 'reg2.html', {'form_obj': form_obj})
```

模板：

```
{{ form_obj.as_p }}   一次性生成所有的input框

{{ form_obj.user }}    		该字段的input框
{{ form_obj.user.label }}   该字段提示的信息
{{ form_obj.user.id_for_label }}    该字段的input框的id
{{ form_obj.user.errors }}      该字段的所有错误 
{{ form_obj.user.errors.0 }}    该字段的第一个错误 

{{ form_obj.errors }}   所有字段的错误


```

常用字段

```
CharField   文本输入框
ChoiceField    单选  默认是select
MultipleChoiceField	  多选  默认是select
```

字段参数

```
initial       默认值
choices      用户选择的数据
error_messages   自定义错误信息
widget  	 插件    修改input框的类型
required	 是否必填
disabled	 是否禁用

```

校验

校验器：

1. 定义函数

   ```
   def check_name(value):
       # 不符合校验规则
       if 'alex' in value:
           raise ValidationError('alex的名字不符合社会主义价值观')
       # 符合校验不做任何操作
       
   user = forms.CharField(
     		...
           validators=[check_name],)
   ```

2. 使用内置的校验器

   ```
   from django.core.validators import RegexValidator
   
   phone = forms.CharField(validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式不正确')])
   ```

钩子函数：

1. 局部钩子

   ```python
   # 一定要写在类中    
       def clean_user(self):
           # 不符合校验规则 抛出异常
           value = self.cleaned_data.get('user')
           if 'alex' in value:
               raise ValidationError('alex的名字不符合社会主义价值观')
           # 符合校验规则   返回该字段的值
           return value
   ```

2. 全局钩子

   ```python
       def clean(self):
           # 全局钩子
           pwd = self.cleaned_data.get('pwd')
           re_pwd = self.cleaned_data.get('re_pwd')
           if pwd != re_pwd:
               # 不符合校验规则 抛出异常
               # 将错误信息加入到某个字段中
               self.add_error('re_pwd','两次密码不一致!!!')
               raise ValidationError('两次密码不一致')
           # 符合校验规则   返回所有字段的值
           return self.cleaned_data
   ```

   

is_valid()的流程：

1. 执行一个full_clean方法

   1. 定义一个 错误字典 和 cleaned_data = {}     # 存在已经经过校验的数据的字典、

   2. 执行self._clean_fields()

      循环所有的字段

      对一个字段进行内置的校验、校验器的校验、局部钩子的校验

      校验不通过，错误字典中有该字段的错误信息

      所有校验通过，self.cleaned_data有该字段的值

   3. 执行全局钩子

