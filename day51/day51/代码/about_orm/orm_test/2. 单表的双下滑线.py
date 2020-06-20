import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "about_orm.settings")
import django
django.setup()
from app01 import models
ret = models.Person.objects.filter(pid__lt=6)  # 字段__条件 =    less than 小于
ret = models.Person.objects.filter(pid__gt=6)  # 字段__条件 =    greater than 大于
ret = models.Person.objects.filter(pid__lte=6)  # 字段__条件 =    less than equal 小于等于
ret = models.Person.objects.filter(pid__gte=6)  # 字段__条件 =    greater than equal 大于等于

ret = models.Person.objects.filter(pid__range=[1,6])    # 范围
ret = models.Person.objects.filter(pid__in=[1,5,6])     # 成员判断

ret = models.Person.objects.filter(name__contains='alex')  # like
ret = models.Person.objects.filter(name__icontains='alex')  # like ignore忽略   忽略大小写

ret = models.Person.objects.filter(name__startswith='aaa')  # 以什么开头
ret = models.Person.objects.filter(name__istartswith='aaa')  # 以什么开头 忽略大小写

ret = models.Person.objects.filter(name__endswith='aaa')  # 以什么结尾
ret = models.Person.objects.filter(name__iendswith='aaa')  # 以什么结尾 忽略大小写

ret = models.Person.objects.filter(birth__year='2019')
ret = models.Person.objects.filter(birth__contains='-01-')

ret = models.Person.objects.filter(name__isnull=True)   # 是否为null
print(ret)