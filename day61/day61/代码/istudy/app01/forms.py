from django import forms
from django.core.exceptions import ValidationError
import hashlib
from app01 import models


class BSForm(forms.ModelForm):
    """
    拥有bootstrap的样式
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义的操作
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


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
        exclude = ['last_time', 'is_active']
        # labels = {
        #     'username': '用户名'
        # }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '用户名', 'autocomplete': 'off'}),
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


class ArticleForm(BSForm):
    class Meta:
        model = models.Article
        fields = "__all__"
        exclude = ['detail']

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'})
        # }

    def __init__(self, request, *args, **kwargs):
        # 获取到用户传来的其他的参数 request  不要往下面的__init__方法传了
        super().__init__(*args, **kwargs)

        # 自定义的操作
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # 修改choices的参数
        self.fields['author'].choices = [(request.user_obj.pk, request.user_obj.username)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 修改choices的参数
        self.fields['author'].choices = [(self.instance.author_id, self.instance.author.username)]


class ArticleDetailForm(forms.ModelForm):
    class Meta:
        model = models.ArticleDetail
        fields = "__all__"


from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget


class ArticleDetailForm(forms.ModelForm):
    class Meta:
        model = models.ArticleDetail
        fields = "__all__"

        widgets = {
            'content': CKEditorUploadingWidget
        }


class CategoryForm(BSForm):
    class Meta:
        model = models.Category
        fields = '__all__'


class SeriesForm(BSForm):
    class Meta:
        model = models.Series
        fields = '__all__'
