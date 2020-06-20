from django.db import models


class MyCharField(models.Field):
    """
    自定义的char类型的字段类
    """

    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(MyCharField, self).__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        """
        限定生成数据库表的字段类型为char，长度为max_length指定的值
        """
        return 'char(%s)' % self.max_length


# Create your models here.
class Person(models.Model):
    pid = models.AutoField(primary_key=True)  # 主键
    name = models.CharField(verbose_name='姓名', unique=True, db_column='nick',
                            max_length=32, null=True, blank=True)  # varchar(32)
    age = models.IntegerField(default=18)
    phone = MyCharField(max_length=11, unique=True)
    gender = models.BooleanField(choices=((True, 'male'), (False, 'female')))
    birth = models.DateTimeField(auto_now=True)

    # auto_now_add=True 新增数据时自动保存当前的时间
    # auto_now=True  新增和编辑数据时自动保存当前的时间

    def __str__(self):
        return "<Person object:{}-{}-{}>".format(self.pk, self.name, self.age)

    __repr__ = __str__

    class Meta:
        # 数据库中生成的表名称 默认 app名称 + 下划线 + 类名
        db_table = "person"

        # admin中显示的表名称
        verbose_name = '个人信息'

        # verbose_name加s
        verbose_name_plural = '所有用户信息'
        #
        # # 联合索引
        # index_together = [
        #     ("name", "age"),  # 应为两个存在的字段
        # ]
        # #
        # # # 联合唯一索引
        # unique_together = (("name", "age"),)  # 应为两个存在的字段


class Publisher(models.Model):
    name = models.CharField(max_length=32, verbose_name="出版社名称")

    def __str__(self):
        return "<Publisher object:{}-{}>".format(self.pk, self.name, )


class Book(models.Model):
    name = models.CharField(max_length=32, verbose_name="书名")
    pub = models.ForeignKey('Publisher', null=True, on_delete=models.CASCADE, related_name='books',
                            related_query_name='book')
    price = models.DecimalField(max_digits=5, decimal_places=2)  # 999.99
    sale = models.IntegerField()
    kucun = models.IntegerField()


    def __str__(self):
        return "<Book object:{}-{}>".format(self.pk, self.name, )


class Author(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    books = models.ManyToManyField('Book', related_name='authors')

    def __str__(self):
        return "<Author object:{}-{}>".format(self.pk, self.name, )
