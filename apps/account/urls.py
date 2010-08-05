from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'my/edit'}),
)

urlpatterns += patterns('',                       
    url(r'^(?P<username>[-\w]+)/detail$', views.detail, name='detail'),
    url(r'dashboard$', views.dashboard, name='dashboard'),
    url(r'^(?P<username>[-\w]+)/edit$', views.edit, name='edit'),
    (r'^register/band', include('account.backends.userband.urls')),
)



