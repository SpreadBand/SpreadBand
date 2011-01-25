from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    # CRUD
    url(r'^new$', views.new, name='create'),
    url(r'^list$', views.list, name='list'),

    # Search
    url(r'^search$', views.search, name='search'),
    url(r'^search/cantfind$', views.search_cantfind, name='search-cantfind'),

    # dashboard
    url(r'^(?P<venue_slug>[-\w]+)/dashboard$', views.dashboard, name='dashboard'),

    # pictures
    url(r'^(?P<venue_slug>[-\w]+)/pictures/new$', views.picture_new, name='picture-new'),

    # membership
    #  url(r'^(?P<venue_slug>[-\w]+)/members/request$', views.members.membership_request, name='membership-request'),
    url(r'^(?P<venue_slug>[-\w]+)/members/add$', views.membership_add, name='membership-add'),
    url(r'^(?P<venue_slug>[-\w]+)/members/(?P<member_id>\d+)/remove$', views.membership_remove, name='membership-remove'),
    url(r'^(?P<venue_slug>[-\w]+)/members/manage$', views.membership_manage, name='membership-manage'),


    url(r'^(?P<venue_slug>[-\w]+)$', views.detail, name='detail'),
    url(r'^(?P<venue_slug>[-\w]+)/edit$', views.edit, name='edit'),

)



