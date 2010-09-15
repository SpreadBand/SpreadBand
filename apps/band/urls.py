from django.conf.urls.defaults import *
from django.conf import settings

import views
import views.members
import views.socialnets

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    url(r'^new$', views.new, name='create'),

    url(r'^list$', views.list, name='list'),

    url(r'^(?P<band_slug>[-\w]+)/edit$', views.edit, name='edit'),

    # pictures
    url(r'^(?P<band_slug>[-\w]+)/pictures$', views.picture_list, name='band-pictures'),
    url(r'^(?P<band_slug>[-\w]+)/pictures/new$', views.picture_new, name='band-picture-new'),
    url(r'^(?P<band_slug>[-\w]+)/pictures/delete/(?P<picture_id>\d+)$', views.picture_delete, name='band-picture-delete'),

    # events
    url(r'^(?P<band_slug>[-\w]+)/events/$', views.event_detail, name='event-detail'),
    url(r'^(?P<band_slug>[-\w]+)/events/new$', views.event_new, name='event-new'),

    # membership
    #  url(r'^(?P<band_slug>[-\w]+)/members/request$', views.members.membership_request, name='membership-request'),
    url(r'^(?P<band_slug>[-\w]+)/members/add$', views.members.membership_add, name='membership-add'),
    url(r'^(?P<band_slug>[-\w]+)/members/(?P<member_id>\d+)/remove$', views.members.membership_remove, name='membership-remove'),
    url(r'^(?P<band_slug>[-\w]+)/members/manage$', views.members.membership_manage, name='membership-manage'),

    # socialnets
    url(r'^(?P<band_slug>[-\w]+)/socialnets/add$', views.socialnets.socialnet_add, name='socialnet-add'),
    url(r'^(?P<band_slug>[-\w]+)/socialnets/edit$', views.socialnets.socialnet_edit, name='socialnet-edit'),

    # (r'^web/', include('minisite.urls', namespace='minisite')),

    url(r'^(?P<band_slug>[-\w]+)/dashboard$', views.dashboard, name='dashboard'),

    # Catch-all for the band name
    url(r'^(?P<band_slug>[-\w]+)/$', views.detail, name='detail'),
)
