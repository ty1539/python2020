## 内容回顾

1. django处理浏览器的请求的流程：

   1. 请求发送到了wsgi，wsgi封装请求的相关数据（request）
   2. django去匹配路径，根据路径判断要执行哪个函数
   3. 执行函数，函数中处理具体的业务逻辑
   4. 函数返回响应，django按照HTTP协议的响应的格式进行返回

2. 发请求的途径

   1. 在浏览器的地址栏中输入地址  回车  ——》  get 
   2. a标签   ——》  get
   3. form表单  post/get 

3. get和post请求的区别

   get    获取一个资源 

   ?k1=v1&k2=v2        request.GET

   get请求没有请求体

   

   post   提交数据

   request.POST 

   数据在请求体中

4. views.py

   ```python
   
   
   def login(request):
   	# 业务逻辑
   	
   	return 响应
   
   
   HttpResponse('字符串')   # 返回一个字符串
   render(request,'模板的文件名'，{‘k1’:v1})
   redirect('地址')  # 重定向
   
   request.method  # 请求方式  GET POST 
   ```

5. ORM

   models.py

   ```python
   
   class Publisher(models.Model):
       name = models.CharField(max_length=32)  # varchar(32)
   	
   
   class Book(models.Model):
       name = models.CharField(max_length=32)  # varchar(32)
       pub = models.ForeignKey('Publisher',on_delete=models.CASCADE)
       """
       on_delete  2.0版本后是必填的 
           models.CASCADE  级联删除
           models.PROTECT  保护
           models.SET(v)   删除后设置为某个值
           models.SETDEFAULT   删除后设置为默认值
           models.SET_NULL     删除后设置为Null
           models.DO_NOTHING  什么都不做
       """
       
   ```

   orm的操作：

   查

   ````python
   from app01 import models
   models.Publisher.objects.all()  # 获取所有的数据  QuerySet  对象列表
   models.Publisher.objects.get(name='xxx',id='1')  # 获取一条存在且唯一的数据  对象
   models.Publisher.objects.filter(name='xxx',id='1')  # 获取多条的数据  对象列表
   
   ret = models.Book.objects.all() # 对象列表
   for book in ret:
   	print(book)
   	print(book.id,book.pk)
   	print(book.name)
   	print(book.pub)      # 书籍所关联的出版社的对象
   	print(book.pub_id)   # 书籍所关联的出版社的id
   
   ````

   新增：

   ```python
   models.Publisher.objects.create(name='xxx')  # 新增的对象
   
   models.Book.objects.create(name='xxx',pub=出版社的对象)   # 新增的对象
   models.Book.objects.create(name='xxx',pub_id=出版社的id)  # 新增的对象
   ```

   删除

   ```
   models.Publisher.objects.get(pk=1).delete()
   models.Publisher.objects.filter(pk=1).delete()  # 批量删除
   ```

   编辑

   ```python
   book_obj.name = 'xxx'
   # book_obj.pub= 出版社对象  
   # book_obj.pub_id= 出版社的id
   book_obj.save()  # 保存到数据库
   
   
   models.Book.objects.filter(pk=1).update(name='xx',pub_id=出版社的id) # 批量更新
   
   ```

6. 模板的语法

   return render(request,'模板的文件名'，{‘k1’:v1,'k2':v2})

   ```html
   {{ k1 }}  {{ k2 }}  
   
   
   for 
   {% for i in k1   %}
   	
   	{{ forloop.counter }}
   	{{ i }}
   
   {% endfor %}
   
   
   if  
   {% if 条件 %}
   	xxx
   {% endif %}
   
   
   {% if 条件 %}
   	xxx
   {% else %}
   	x1
   {% endif %}
   
   
   {% if 条件 %}
   	xxx
   {% elif 条件1 %}	
   	xx
   {% else %}
   	x1
   {% endif %}
   ```

   

作者表增删改查

```python
# 作者表
class Author(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToManyField('Book')  # 不在Author表中新增字段，会创建第三章表

```

```python
    all_authors = models.Author.objects.all()
    for author in all_authors:
        print(author)
        print(author.id)
        print(author.name)
        print(author.books)  # 关系管理对象
        print(author.books.all())  # 所关联的所有的对象
        print('*' * 40)
```

展示

```html
<table border="1">
    <thead>
    <tr>
        <th>序号</th>
        <th>ID</th>
        <th>姓名</th>
        <th>代表作</th>
    </tr>

    </thead>
    <tbody>

    {% for author in all_authors %}
        <tr>
            <td>{{ forloop.counter }}</td>
            <td>{{ author.pk }}</td>
            <td>{{ author.name }}</td>
            <td>
                {% for book in author.books.all %}
                    《 {{ book.name }} 》
                {% endfor %}
            </td>
        </tr>
    {% endfor %}
    
    </tbody>
</table>
```

新增

```python
author_name = request.POST.get('author_name')
book_ids = request.POST.getlist('book_ids')  # 获取多个数据 list类型
# print(book_ids,type(book_ids))

# 向作者表插入了作者的信息
author_obj = models.Author.objects.create(name=author_name)
# 该作者和提交的书籍绑定多对多的关系
author_obj.books.set(book_ids)  # 设置多对多关系
```

编辑

```python
author_name = request.POST.get('author_name')
book_ids = request.POST.getlist('book_ids')
# 给该对象修改数据
# 修改作者的姓名
author_obj.name = author_name
author_obj.save()
# 修改作者和书的多对多关系
author_obj.books.set(book_ids)  # 重新设置
```