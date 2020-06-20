## 新增和编辑

路由

```
url(r'^category_add/$', views.category_change, name='category_add'),
url(r'^category_edit/(\d+)$', views.category_change, name='category_edit'),
```

视图

```
def category_change(request, pk=None):
    obj = models.Category.objects.filter(pk=pk).first()  # pk=None   obj=>None
    form_obj = CategoryForm(instance=obj)
    if request.method == 'POST':
        form_obj = CategoryForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('category_list')

    title = '编辑分类' if pk else '新增分类'

    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})
```

模板

```HTML
{% extends 'dashboard.html' %}


{% block main %}
    <h1>{{ title }}</h1>

    <form class="form-horizontal" method="post" action="" novalidate>
        {% csrf_token %}

        {% for field in form_obj %}
            <div class="form-group {% if field.errors %}has-error{% endif %}">

                <label for="{{ field.id_for_label }}"
                       class="col-sm-2 control-label">{{ field.label }}</label>
                <div class="col-sm-8">
                    {{ field }}
                    <span class="help-block"> {{ field.errors.0 }} </span>
                </div>
            </div>
        {% endfor %}

        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
                <button type="submit" class="btn btn-default">保存</button>
            </div>
        </div>
    </form>

{% endblock %}

```






Q

```
q = Q()
# Q(Q(title__contains=query)|Q(detail__content__contains=query))
q.connector = 'OR'
q.children.append(Q(title__contains=query))
q.children.append(Q(detail__content__contains=query))


Q(title__contains=query)  #   Q(('title__contains',query))
 


def get_query(request, field_list):
    # 传入一个列表['title','detail__content'] ,返回一Q对象
    query = request.GET.get('query', '')

    q = Q()
    # Q(Q(title__contains=query)|Q(detail__content__contains=query))
    q.connector = 'OR'
    for field in field_list:

        q.children.append(Q(('{}__contains'.format(field),query)))
    # q.children.append(Q(detail__content__contains=query))

    return q

```



```
from django.http.request import QueryDict

request.GET._mutable = True
request.GET['page'] = 1

request.GET.copy()  # 返回一个可编辑的深拷贝

request.GET.urledncode()  # page=1&aa=111
```



