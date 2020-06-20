import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "about_orm.settings")
import django

django.setup()
from app01 import models
from django.db.models import F
from django.db import transaction

try:
    with transaction.atomic():
        # 一系列的操作
        models.Book.objects.all().update(kucun=F('kucun') - 10)
        models.Book.objects.all().update(sale=F('sale') + 10)
except Exception as e:
    print(e)
