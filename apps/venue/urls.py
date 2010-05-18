from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    url(r'^new$', views.new, name='create'),
    url(r'^list$', views.list, name='list'),
    url(r'^(?P<venue_slug>[-\w]+)$', views.detail, name='detail'),
)


