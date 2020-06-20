import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "about_orm.settings")
import django

django.setup()
from app01 import models

# 基于对象的查询
# 正向查询
book_obj = models.Book.objects.get(pk=1)
# print(book_obj.pub)  # 关联的出版社对象
# print(book_obj.pub_id)  # 关联的出版社的id

# 反向查询
pub_obj = models.Publisher.objects.get(pk=1)
# 没有指定related_name  类名小写_set
# print(pub_obj)
# print(pub_obj.book_set,type(pub_obj.book_set))   # 类名小写_set   关系管理对象
# print(pub_obj.book_set.all())

# 指定related_name='books'  没有 类名小写_set 的写法

print(pub_obj.books.all())

# 基于字段的查询
ret = models.Book.objects.filter(pub__name='新华出版社')

# 不指定related_name='books'    类名小写
# ret = models.Publisher.objects.filter(book__name='坐在床上学xx')

# 指定related_name='books'  不指定related_query_name
# ret = models.Publisher.objects.filter(books__name='坐在床上学xx')

# 指定related_query_name='book'

ret = models.Publisher.objects.filter(book__name='坐在床上学xx')

# print(ret)

# set  add  create   只有对象 没有id
# pub_obj.books.set(models.Book.objects.filter(id__in=[1,2,3,4] ))
pub_obj.books.add(*models.Book.objects.all())

# remove clear  ForeignKey('Publisher',null=True,)
# pub_obj.books.clear()
