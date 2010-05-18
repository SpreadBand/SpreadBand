from django.conf.urls.defaults import *
from django.conf import settings

import views.event_bargain
import views.calendar

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    url(r'^gig/new/(?P<band_slug>[-\w]+)/$', views.calendar.gig_create, name='gig-new'),

    url(r'^calendar/band/(?P<band_slug>[-\w]+)/$', views.calendar.band_calendar_detail, name='band-calendar'),
    url(r'^calendar/venue/(?P<venue_slug>[-\w]+)/$', views.calendar.venue_calendar_detail, name='venue-calendar'),

    # Bargain
    url(r'^bargain/new/(?P<venue_slug>[-\w]+)/$', views.event_bargain.event_bargain_new, name='bargain-new'),

    # Bargain, band specific
    url(r'^bargain/(?P<contract_id>\d+)/approve/band/(?P<band_slug>[-\w]+)$', views.event_bargain.event_bargain_approve_band, name='bargain-approve-band'),
    url(r'^bargain/(?P<contract_id>\d+)/disapprove/band/(?P<band_slug>[-\w]+)$', views.event_bargain.event_bargain_disapprove_band, name='bargain-disapprove-band'),

    # Bargain, venue specific
    url(r'^bargain/(?P<contract_id>\d+)/approve/venue/(?P<venue_slug>[-\w]+)$', views.event_bargain.event_bargain_approve_venue, name='bargain-approve-venue'),
    url(r'^bargain/(?P<contract_id>\d+)/disapprove/venue/(?P<venue_slug>[-\w]+)$', views.event_bargain.event_bargain_disapprove_venue, name='bargain-disapprove-venue'),

    url(r'^bargain/(?P<contract_id>\d+)/update$', views.event_bargain.event_bargain_update, name='bargain-update'),
    url(r'^bargain/(?P<contract_id>\d+)/detail$', views.event_bargain.event_bargain_detail, name='bargain-detail'),
)


