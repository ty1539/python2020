## 内容回顾

form组件

form

```python
# 定义form
form django import forms

class RegForm(forms.Form):
    user = forms.CharField(
        label='用户名',
        min_length=11,
        inital='初始值',
        required=True,
        disabled=False,
        error_messages={
            'required':'xxxx',
            'min_length':'xxssw'
        }
        validators=[自定义的函数,内置的校验器]
        
    )
    password = forms.CharField(widget=forms.PasswordInput)

    
url(^'reg',reg)
    
  
def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        # 对提交的数据进行校验
        if form_obj.is_valid():
            # 校验成功做的操作
            form_obj.cleaned_data   # request.POST
    
    return  render(request,'reg.html',{'form_obj':form_obj})
```

```html


<form  action='' methond='post' >

{% csrf_token %}



{{ form_obj.user }}          input框
{{ form_obj.user.label }}    label提示信息
{{ form_obj.user.id_for_label }}     input框的id
{{ form_obj.user.errors }}      某个字段的所有错误 
{{ form_obj.user.errors.0 }}    某个字段的第一个错误 


{{ form_obj.errors }}    所有字段的所有错误 

<button>注册</button>
</form>


```

校验

校验器：

1. 写函数

   ```python
   from django.core.exceptions import ValidationError
   def xxx(value):
       # 写校验规则
       # 校验成功 什么都不做 return
       # 校验失败 抛出异常 ValidationError('提示信息')
   
   ```

2. 内置的校验器

   from django.core.validators import RegexValidator

钩子函数：

1. 局部钩子

   ```python
   
   class RegForm(forms.Form):
       user = forms.CharField()    
       
       def clean_user(self):
       	# 校验
           # 校验成功  返回该字段的值
           # 校验失败  抛出异常 
   
   ```

2. 全局钩子

   ```python
   class RegForm(forms.Form):
       user = forms.CharField()
       
       
       def clean(self):
       	# 校验
           # 校验成功  返回所有字段的值  self.cleaned_data
           # 校验失败  抛出异常 
   ```

   

定义的modelform

```python
from django import forms


class RegForm(forms.ModelForm):
    # username = forms.CharField()class RegForm(forms.ModelForm):
    # username = forms.CharField(label='xxx')
    # password = forms.CharField()
    password = forms.CharField(error_messages={'required': '这是必选项'}, widget=forms.PasswordInput, label='密码',
                               min_length=6)
    re_pwd = forms.CharField(widget=forms.PasswordInput, label='确认密码', min_length=6)

    class Meta:
        model = models.User
        fields = '__all__'  # ['username','password']
        exclude = ['last_time']
        # labels = {
        #     'username': '用户名'
        # }
        widgets = {
            'password': forms.PasswordInput
        }
        error_messages = {
            'username': {
                'required': '必填项',
            },
            'password': {
                'required': '必填项',
            }
        }

    def clean_phone(self):
        import re
        phone = self.cleaned_data.get('phone')
        if re.match(r'^1[3-9]\d{9}$', phone):
            return phone
        raise ValidationError('手机号格式不正确')

    def clean(self):
        self._validate_unique = True  # 数据库校验唯一
        password = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_pwd')

        if password == re_pwd:
            return self.cleaned_data
        self.add_error('re_pwd', '两次密码不一致！！')
        raise ValidationError('两次密码不一致')

```



