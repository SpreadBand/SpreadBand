from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    (r'^web/', include('minisite.urls', namespace='minisite')),

    (r'^new$', 'bands.views.new'),
    (r'^list$', 'bands.views.list'),

    (r'^(?P<band_id>\d+)$', views.detail),
    (r'^(?P<band_id>\d+)/', include('photologue.urls')),
    (r'^(?P<band_id>\d+)/membership/request', 'bands.views.membership_request'),
    (r'^(?P<band_id>\d+)/bargain/', include('bargain.urls')),
)
