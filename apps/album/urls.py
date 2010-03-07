from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',                       
   url(r'^$', views.album_list, name='list'),
   url(r'^create$', views.album_create, name='create'),
   url(r'^(?P<album_id>\d+)/edit$', views.album_edit, name='edit'),
   url(r'^(?P<album_id>\d+)/edit-one$', views.album_edit_one, name='edit-one'),
   url(r'^(?P<album_id>\d+)$', views.album_details, name='detail'),

   url(r'^(?P<album_id>\d+)/track/new$', views.track_new, name='track-new'),
   url(r'^(?P<album_id>\d+)/track/(?P<track_id>\d+)/delete$', views.track_delete, name='track-delete'),
)



