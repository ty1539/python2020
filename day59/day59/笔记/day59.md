展示数据的方法：

数据对象  obj  

1. 普通字段

   obj.字段名     ——》  数据库该字段的值

2. 带choices参数的

   obj.字段名     ——》  数据库该字段的值

   `obj.get_字段名_display()  `   要显示的结果

3. 外键

   obj.外键   ——》 所关联的对象  `   __str__`方法

   obj.外键.字段

4. 自定义方法

   ```python
   from django.utils.safestring import mark_safe
   def show_publish_status(self):
       color_dict = {True: 'green', False: '#c35353'}
   
       return mark_safe(
           '<span style="background: {};color: white;padding: 3px" >{}</span>'.format(color_dict[self.publish_status],
                                                                                      self.get_publish_status_display()))
   ```





定义modelform

```python
class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = "__all__"
        exclude = ['detail']

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义的操作
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
```

使用form

```python
def article_add(request):
    form_obj = ArticleForm()
    if request.method == 'POST':
        form_obj = ArticleForm(request.POST)
        if form_obj.is_valid():
            #  获取文章详情的字符串
            detail = request.POST.get('detail')
            #  创建文章详情的对象
            detail_obj = models.ArticleDetail.objects.create(content=detail)
            form_obj.instance.detail_id = detail_obj.pk
            form_obj.save()  # form_obj.instance.save()
            return redirect('article_list')

    return render(request, 'article_add.html', {'form_obj': form_obj})


# 编辑文章
def article_edit(request, pk):
    obj = models.Article.objects.filter(pk=pk).first()
    form_obj = ArticleForm(instance=obj)
    if request.method == 'POST':
        form_obj = ArticleForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.instance.detail.content = request.POST.get('detail')
            form_obj.instance.detail.save()   # 保存文章详情
            form_obj.save()   # 保存文章的信息
            return redirect('article_list')

    return render(request, 'article_edit.html', {'form_obj': form_obj, 'obj': obj})



#  HTML


{% for field in form_obj %}

    {{ field.id_for_label }}
    
    {{ field.label }}

    {{ field }}    input框
    
    {{ field.errors.0 }}

{% endfor %}


```



让用户上传头像

```python
model中添加ImageField
avatar = models.ImageField(upload_to='img/avatar',default='img/avatar/dafault.jpeg')

# ImageField  依赖 pillow模块  pip install pillow
```



media的配置

seetings.py

```
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
```

urls.py

```python
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app01.urls')),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]
```



使用django-ckeditor

https://pypi.org/project/django-ckeditor/

1. 下载

   pip install django-ckeditor

2. 注册app

   ```
   INSTALLED_APPS = [
    	...
       'ckeditor',
       'ckeditor_uploader',
   ]
   ```

3. urls.py

   ```
   urlpatterns = [
      ...
       url(r'^ckeditor/', include('ckeditor_uploader.urls')),
   ]
   ```

4. models.py

   ```
   class ArticleDetail(models.Model):
       """
       文章详情
       """
       content = RichTextUploadingField(verbose_name='文章内容')
   ```

5. modelform

   ```
   class ArticleDetailForm(forms.ModelForm):
       class Meta:
           model = models.ArticleDetail
           fields = "__all__"
           
           
           
   form_obj = ArticleDetailForm()
   ```

6. html

   {{   form_obj. content  }}

   引入静态文件

   ```hsml
   {% load static %}
   <script type="text/javascript" src="{% static "ckeditor/ckeditor-init.js" %}"></script>
   <script type="text/javascript" src="{% static "ckeditor/ckeditor/ckeditor.js" %}"></script>
   ```

7. 上传文件需要认证，取消认证

   ```python 
   # 将staff_member_required装饰器取消掉即可
   urlpatterns = [
       url(r'^upload/', staff_member_required(views.upload), name='ckeditor_upload'),
       url(r'^browse/', never_cache(staff_member_required(views.browse)), name='ckeditor_browse'),
   ]
   ```

   