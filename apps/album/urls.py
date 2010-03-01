from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',                       
   url(r'^$', views.album_list, name='list'),
   url(r'^create$', views.album_create, name='create'),
   url(r'^(?P<album_id>\d+)$', views.album_details, name='detail'),
)



