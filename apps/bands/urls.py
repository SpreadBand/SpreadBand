from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    (r'^new$', 'bands.views.new'),
    (r'^list$', 'bands.views.list'),
    (r'^view/(?P<band_id>\d+)$', views.detail),
    (r'^view/(?P<band_id>\d+)/', include('photologue.urls')),
)
