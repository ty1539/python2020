from django.shortcuts import render, HttpResponse


# Create your views here.
def reg(request):
    if request.method == 'POST':
        # 获取提交的数据
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        # 对数据进行校验
        if len(user) < 6:
            # 校验不通过  返回错误的提示
            user_error = '用户名长度不能小于6位'
            return render(request, 'reg.html', locals())
        else:
            # 校验通过 插入数据库
            return HttpResponse('注册成功')

    return render(request, 'reg.html')


from django import forms
from django.forms import models as form_model
from app01 import models

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def check_name(value):
    # 不符合校验规则
    if 'alex' in value:
        raise ValidationError('alex的名字不符合社会主义价值观')
    # 符合校验不做任何操作


class RegForm(forms.Form):
    user = forms.CharField(
        label='用户名',
        required=False,
        disabled=True,
        min_length=6,
        initial="alexdsb",
        # validators=[check_name],
        error_messages={
            "required": "不能为空",
            "min_length": "用户名最短6位"
        }
    )
    pwd = forms.CharField(label='密码', widget=forms.PasswordInput)
    re_pwd = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=(('1', '男'), ('2', '女'), ('3', '不详')))
    # hobby = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=(('1', '抽烟'), ('2', '喝酒'), ('3', '画大饼')))
    # hobby = form_model.ModelMultipleChoiceField(queryset=models.Hobby.objects.all(),widget=forms.CheckboxSelectMultiple)
    hobby = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    phone = forms.CharField(validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式不正确')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hobby'].choices = models.Hobby.objects.values_list('id', 'name')

    def clean_user(self):
        # 不符合校验规则 抛出异常
        value = self.cleaned_data.get('user')
        if 'alex' in value:
            raise ValidationError('alex的名字不符合社会主义价值观')
        # 符合校验规则   返回该字段的值
        return value

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


def reg2(request):
    form_obj = RegForm()
    if request.method == 'POST':
        # 对提交的数据做校验
        form_obj = RegForm(request.POST)

        if form_obj.is_valid():  # 对数据进行校验
            # 校验成功
            return HttpResponse('注册成功')
        print(form_obj.cleaned_data)  # 经过校验没有问题的数据
    return render(request, 'reg2.html', {'form_obj': form_obj})
