import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "about_orm.settings")
import django

django.setup()
from app01 import models

from django.db.models import F, Q

ret = models.Book.objects.filter(kucun__lt=50)

ret = models.Book.objects.filter(sale__gt=F('kucun'))  # where  'sale' > 'kucun'

# ret = models.Book.objects.filter(id__lte=3).update(sale=F('sale') * 2 + 13)

# Q()
# |   或
# &   与
# ~   非

ret = models.Book.objects.filter(Q(id__lt=3) | Q(id__gt=5))

ret = models.Book.objects.filter(Q(Q(id__lt=3) | Q(id__gt=5))&Q(name__startswith='天然'))

ret = models.Book.objects.filter(Q(Q(id__lt=3) | Q(id__gt=5))&~Q(name__startswith='天然'))


print(ret)
