from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
]
