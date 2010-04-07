from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',                       
   url(r'^(?P<band_slug>[-\w]+)/album/$', views.album_list, name='list'),
   url(r'^(?P<band_slug>[-\w]+)/album/create$', views.album_create, name='create'),
   url(r'^(?P<band_slug>[-\w]+)/album/(?P<album_slug>[-\w]+)/edit$', views.album_edit, name='edit'),
   url(r'^(?P<band_slug>[-\w]+)/album/(?P<album_slug>[-\w]+)/edit-one$', views.album_edit_one, name='edit-one'),
   url(r'^(?P<band_slug>[-\w]+)/album/(?P<album_slug>[-\w]+)/$', views.album_details, name='detail'),

   url(r'^(?P<band_slug>[-\w]+)/album/(?P<album_slug>[-\w]+)/track/new$', views.track_new, name='track-new'),
   url(r'^(?P<band_slug>[-\w]+)/album/(?P<album_slug>[-\w]+)/track/(?P<track_id>\d+)/delete$', views.track_delete, name='track-delete'),
)



