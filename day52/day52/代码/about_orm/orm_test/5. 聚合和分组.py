import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "about_orm.settings")
import django

django.setup()
from app01 import models

from django.db.models import Max, Min, Count, Sum, Avg

# 聚合 aggregate  终止子句
ret = models.Book.objects.filter(id__gt=2).aggregate(min=Min('price'),
                                                     max=Max('price'))  # {'price__max': Decimal('999.00')}

#  分组   group by
# annotate  注释   过程中使用了分组
# 统计每一本书的作者个数
ret = models.Book.objects.annotate(Count('authors')).values()  # 添加额外的信息

# 统计出每个出版社卖的最便宜的书的价格
# 方法一
ret = models.Publisher.objects.annotate(Min('book__price')).values()
# for i in ret:
#     print(i)
# 方法二

# ret = models.Book.objects.annotate(Min('price')).values()  # 错误写法  按照书分组
# 按照 pub_id  pub__name 分组
# ret = models.Book.objects.values('pub','pub__name').annotate(min=Min('price'))

# for i in ret:
#     print(i)


# 统计不止一个作者的图书
ret = models.Book.objects.annotate(count=Count('authors')).filter(count__gt=1)
# print(ret)

# 根据一本图书作者数量的多少对查询集 QuerySet进行排序
ret = models.Book.objects.annotate(count=Count('authors')).order_by('-count')

# print(ret)

# 查询各个作者出的书的总价格
ret = models.Author.objects.annotate(sum=Sum('books__price')).values()


ret = models.Book.objects.values('authors','authors__name').annotate(sum=Sum('price'))
for i in ret:
    print(i)


