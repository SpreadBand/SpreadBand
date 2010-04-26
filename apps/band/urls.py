from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    url(r'^new$', views.new, name='create'),

    url(r'^list$', views.list, name='list'),

    url(r'^(?P<band_slug>[-\w]+)/edit$', views.edit, name='edit'),

    # pictures
    url(r'^(?P<band_slug>[-\w]+)/pictures/new$', views.picture_new, name='picture-new'),

    # events
    url(r'^(?P<band_slug>[-\w]+)/events/$', views.event_detail, name='event-detail'),
    url(r'^(?P<band_slug>[-\w]+)/events/new$', views.event_new, name='event-new'),

    # membership
    url(r'^(?P<band_slug>[-\w]+)/membership/request$', views.membership_request, name='membership-request'),

    # bargain
    url(r'^(?P<band_slug>[-\w]+)/bargain/$', views.event_bargain_new, name='event-bargain-new'),
    url(r'^(?P<band_slug>[-\w]+)/bargain/(?P<contract_id>\d+)/approve$', views.event_bargain_approve, name='event-bargain-approve'),
    url(r'^(?P<band_slug>[-\w]+)/bargain/(?P<contract_id>\d+)/disapprove$', views.event_bargain_disapprove, name='event-bargain-disapprove'),
    url(r'^(?P<band_slug>[-\w]+)/bargain/(?P<contract_id>\d+)/update$', views.event_bargain_update, name='event-bargain-update'),
    url(r'^(?P<band_slug>[-\w]+)/bargain/(?P<contract_id>\d+)/detail$', views.event_bargain_detail, name='event-bargain-detail'),

    (r'^web/', include('minisite.urls', namespace='minisite')),

    # Catch-all for the band name
    url(r'^(?P<band_slug>[-\w]+)/$', views.detail, name='detail'),
)
