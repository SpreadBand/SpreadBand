from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    (r'^new$', 'bands.views.new'),
    (r'^list$', 'bands.views.list'),

    url(r'^(?P<band_id>\d+)/$', views.detail, name='detail'),

    (r'^(?P<band_id>\d+)/membership/request', 'bands.views.membership_request'),
    (r'^(?P<band_id>\d+)/bargain/', include('bargain.urls')),


    url(r'^(?P<band_id>\d+)/album/', include('album.urls', namespace='album')),

    (r'^(?P<band_id>\d+)/', include('photologue.urls')),
    (r'^web/', include('minisite.urls', namespace='minisite')),
)
