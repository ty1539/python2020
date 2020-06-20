from django.db import models


# Create your models here.
class User(models.Model):
    """
    员工信息表用户、密码、职位、公司名（子、总公司）、手机、最后一次登录时间。
    """
    username = models.CharField(max_length=32, verbose_name='用户名',unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    position = models.CharField(max_length=32, verbose_name='职位')
    company = models.CharField(max_length=32, verbose_name='公司',
                               choices=(('0', '北京总公司'), ('1', '石家庄分公司'), ('2', '广州分公司')))
    phone = models.CharField(max_length=11, verbose_name='手机号')
    last_time = models.DateTimeField(null=True, blank=True, verbose_name='上次登陆时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    # class Meta:
    #     db_table =''
