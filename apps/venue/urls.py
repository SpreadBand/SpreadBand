from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    url(r'^new$', views.new, name='create'),
    url(r'^list$', views.list, name='list'),
    url(r'^search$', views.search, name='search'),
    url(r'^search/cantfind$', views.search_cantfind, name='search-cantfind'),

    url(r'^(?P<venue_slug>[-\w]+)$', views.detail, name='detail'),
    url(r'^(?P<venue_slug>[-\w]+)/edit$', views.edit, name='edit'),

    # pictures
    url(r'^(?P<venue_slug>[-\w]+)/pictures/new$', views.picture_new, name='picture-new'),

)



