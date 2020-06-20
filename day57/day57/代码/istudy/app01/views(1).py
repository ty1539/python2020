from django.shortcuts import render, redirect
from app01 import models


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))

        user_obj = models.User.objects.filter(username=username, password=md5.hexdigest(),is_active=True).first()
        if user_obj:
            # 登陆成功
            return redirect('index')
        error = '用户名或密码错误'
    return render(request, 'login.html', locals())


from django import forms
from django.core.exceptions import ValidationError
import hashlib


class RegForm(forms.ModelForm):
    # username = forms.CharField(label='xxx')
    # password = forms.CharField()
    password = forms.CharField(error_messages={'required': '这是必选项'},
                               widget=forms.PasswordInput(attrs={'placeholder': '密码', 'type': 'password'}), label='密码',
                               min_length=6)
    re_pwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '确认密码', 'type': 'password'}),
                             label='确认密码', min_length=6)

    class Meta:
        model = models.User
        fields = '__all__'  # ['username','password']
        exclude = ['last_time']
        # labels = {
        #     'username': '用户名'
        # }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '用户名','autocomplete':'off'}),
            'position': forms.TextInput(attrs={'placeholder': '请输入职位'}),
            # 'company':forms.Select(),
            'phone': forms.TextInput(attrs={'placeholder': '手机号'}),
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

    def clean_company(self):
        # 不符合校验规则 抛出异常
        print(self.cleaned_data)
        value = self.cleaned_data.get('company')
        if not value:
            raise ValidationError('公司是必选项,请重新选择')
        return value

    def clean(self):
        self._validate_unique = True  # 数据库校验唯一
        password = self.cleaned_data.get('password', '')
        re_pwd = self.cleaned_data.get('re_pwd')

        if password == re_pwd:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data
        self.add_error('re_pwd', '两次密码不一致！！')
        raise ValidationError('两次密码不一致')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义的操作
        field = self.fields['company']
        choices = field.choices
        choices[0] = ('', '选择公司')
        field.choices = choices


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
    # 查询所有的文章

    all_article = models.Article.objects.all()
    return render(request, 'index.html',{'all_article':all_article})


def article(request,pk):
    article_obj = models.Article.objects.get(pk=pk)
    return render(request, 'article.html',{'article_obj':article_obj})

