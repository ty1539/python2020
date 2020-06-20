from django.conf.urls import url

from app01 import views

urlpatterns = [

    url(r'^index/$', views.index,),  # /app01/blog/    ——》 blog
    url(r'^home/$', views.home,name='home'),  # /app01/blog/    ——》 blog
    url(r'^blog/$', views.blog,name='blog'),  # /app01/blog/    ——》 blog
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>\d{2})/$', views.blogs,name='blogs'),
]
