from django.conf.urls.defaults import patterns, url
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    # CRUD
    url(r'^new$', views.new, name='create'),

    # Search
    url(r'^search$', views.search, name='search'),
    url(r'^search/cantfind$', views.search_cantfind, name='search-cantfind'),

    # dashboard
    url(r'^(?P<venue_slug>[-\w]+)/dashboard$', views.dashboard, name='dashboard'),
    url(r'^(?P<venue_slug>[-\w]+)/myprofile$', views.my_public_view, name='myprofile'),
    url(r'^(?P<venue_slug>[-\w]+)/profile$', views.public_view, name='profile'),

    # Presskit tracker
    url(r'^(?P<venue_slug>[-\w]+)/presskit/viewrequest/(?P<viewrequest_id>\d+)$', views.presskit_viewrequest_venue, name='presskit-viewrequest-venue'),
    url(r'^(?P<venue_slug>[-\w]+)/presskit/viewrequest/(?P<viewrequest_id>\d+)/venue_comment$', views.presskit_viewrequest_venue_comment, name='presskit-viewrequest-venue-comment'),
    url(r'^(?P<venue_slug>[-\w]+)/presskit/viewrequest/(?P<viewrequest_id>\d+)/accept$', views.presskit_viewrequest_venue_accept, name='presskit-viewrequest-venue-accept'),
    url(r'^(?P<venue_slug>[-\w]+)/presskit/viewrequest/(?P<viewrequest_id>\d+)/refuse$', views.presskit_viewrequest_venue_refuse, name='presskit-viewrequest-venue-refuse'),

    # pictures
    url(r'^(?P<venue_slug>[-\w]+)/pictures$', views.picture_list, name='venue-pictures'),
    url(r'^(?P<venue_slug>[-\w]+)/pictures/new$', views.picture_new, name='venue-picture-new'),
    url(r'^(?P<venue_slug>[-\w]+)/pictures/delete/(?P<picture_id>\d+)$', views.picture_delete, name='venue-picture-delete'),

    # membership
    #  url(r'^(?P<venue_slug>[-\w]+)/members/request$', views.members.membership_request, name='membership-request'),
    url(r'^(?P<venue_slug>[-\w]+)/members/add$', views.membership_add, name='membership-add'),
    url(r'^(?P<venue_slug>[-\w]+)/members/(?P<member_id>\d+)/remove$', views.membership_remove, name='membership-remove'),
    url(r'^(?P<venue_slug>[-\w]+)/members/manage$', views.membership_manage, name='membership-manage'),


    url(r'^(?P<venue_slug>[-\w]+)$', views.detail, name='detail'),
    url(r'^(?P<venue_slug>[-\w]+)/edit$', views.edit, name='edit'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^list$', views.list, name='list'),
                            )



