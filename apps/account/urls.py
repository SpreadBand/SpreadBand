from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'detail'}),
)

urlpatterns += patterns('',                       
    url(r'^detail$', views.detail, name='detail'),
)



