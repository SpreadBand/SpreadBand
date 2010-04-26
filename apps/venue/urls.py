from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    (r'^new$', views.new),
    (r'^list$', views.list),
    (r'^detail/(?P<venue_id>\d+)$', views.detail),
)



