from django.conf.urls.defaults import url, patterns
from django.conf import settings

import views

urlpatterns = patterns('',
    url(r'^(?P<band_slug>[-\w]+)/presskit$', views.presskit_detail, name='presskit-detail'),
    url(r'^(?P<band_slug>[-\w]+)/mypresskit$', views.mypresskit, name='mypresskit'),

    url(r'^(?P<band_slug>[-\w]+)/presskit/video$', views.video_edit, name='presskit-video'),

    url(r'^(?P<band_slug>[-\w]+)/presskit/tracks$', views.track_list, name='presskit-tracks'),
    url(r'^(?P<band_slug>[-\w]+)/presskit/tracks/delete/(?P<track_id>\d+)$', views.track_delete, name='presskit-track-delete'),
    url(r'^(?P<band_slug>[-\w]+)/presskit/tracks/add$', views.track_add, name='presskit-track-add'),
)






