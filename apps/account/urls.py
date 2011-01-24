from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

import userena.views as userena_views

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'dashboard'}),
)

urlpatterns += patterns('',                       

    url(r'^profile/avatar$', views.avatar_set, name='avatar'),

    url(r'dashboard/$', views.dashboard, name='dashboard'),

    url(r'^signup/$', views.signup, name='userena_signup'),
    url(r'^signin/$', userena_views.signin, name='userena_signin'),

    url(r'^signout/$', views.logout, name='userena_signout'),

    url(r'^(?P<username>[-\w]+)/$', views.detail, name='userena_profile_detail'),
    url(r'^(?P<username>[-\w]+)/edit/$', views.edit, name='userena_profile_edit'),
    url(r'^(?P<username>\w+)/password/complete/$', views.password_change_complete, name='userena_password_change_complete'),



)
