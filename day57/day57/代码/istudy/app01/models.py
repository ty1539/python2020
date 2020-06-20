from django.db import models


# Create your models here.
class User(models.Model):
    """
    员工信息表用户、密码、职位、公司名（子、总公司）、手机、最后一次登录时间。
    """
    username = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    position = models.CharField(max_length=32, verbose_name='职位')
    company = models.CharField(max_length=32, verbose_name='公司', blank=True,
                               choices=(('0', '北京总公司'), ('1', '石家庄分公司'), ('2', '广州分公司')))
    phone = models.CharField(max_length=11, verbose_name='手机号')
    last_time = models.DateTimeField(null=True, blank=True, verbose_name='上次登陆时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    is_active = models.BooleanField(default=True)


class Category(models.Model):
    title = models.CharField(max_length=64, verbose_name='板块标题')


class Article(models.Model):
    """
    文章
        标题  文章摘要  作者  板块 创建时间  更新时间  删除状态
    """
    title = models.CharField(max_length=64, verbose_name='文章标题')
    abstract = models.CharField(max_length=256)
    author = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, verbose_name='作者')
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_status = models.BooleanField(default=False, verbose_name='删除状态')

    detail = models.OneToOneField('ArticleDetail', on_delete=models.DO_NOTHING)


class ArticleDetail(models.Model):
    """
    文章详情
    """
    content = models.TextField(verbose_name='文章内容')


class Comment(models.Model):
    """
    评论表
        评论者  评论内容  评论文章  时间  审核状态
    """
    author = models.ForeignKey(verbose_name='评论者', to='User', on_delete=models.DO_NOTHING)
    content = models.TextField(verbose_name='评论内容')
    article = models.ForeignKey(verbose_name='文章', to='Article', on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(verbose_name='审核状态', default=True)
