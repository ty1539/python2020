from django.conf.urls import url

from app02 import views

urlpatterns = [

    url(r'^home/$', views.home, name='home'),
    url(r'^article/$', views.article),  # /app01/blog/
    url(r'^article/(?P<year>[0-9]{4})/(?P<month>\d{2})/$', views.articles, ),
]
