from django.conf.urls import url
from app01 import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^article/(\d+)$', views.article, name='article'),

    url(r'^backend/$', views.backend, name='backend'),

    url(r'^article_list/$', views.article_list, name='article_list'),
    url(r'^article_add/$', views.article_add, name='article_add'),
    url(r'^article_edit/(\d+)/$', views.article_edit, name='article_edit'),

    url(r'^user_list/$', views.user_list, name='user_list'),

    url(r'^category_list/$', views.category_list, name='category_list'),
    # url(r'^category_add/$', views.category_add, name='category_add'),
    # url(r'^category_edit/(\d+)$', views.category_edit, name='category_edit'),

    url(r'^category_add/$', views.category_change, name='category_add'),
    url(r'^category_edit/(\d+)$', views.category_change, name='category_edit'),

]
