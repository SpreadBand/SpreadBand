from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'dashboard'}),
)

urlpatterns += patterns('',                       
    url(r'^(?P<username>[-\w]+)$', views.detail, name='detail'),
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'^(?P<username>[-\w]+)/edit$', views.edit, name='edit'),
    url(r'^profile/avatar$', views.avatar_set, name='avatar'),
    url(r'^profile/password$', views.password, name='password'),
    (r'^register/band', include('account.backends.userband.urls')),
)



