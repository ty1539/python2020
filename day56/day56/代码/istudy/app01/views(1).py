from django.shortcuts import render, redirect
from app01 import models


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.User.objects.filter(username=username, password=password).first()
        if user_obj:
            # 登陆成功
            return redirect('index')
        error = '用户名或密码错误'
    return render(request, 'login.html', locals())


from django import forms
from django.core.exceptions import ValidationError


class RegForm(forms.ModelForm):
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


def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # 注册成功

            form_obj.save()
            return redirect('login')

    return render(request, 'register.html', {'form_obj': form_obj})


def index(request):
    return render(request, 'index.html')
