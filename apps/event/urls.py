from django.conf.urls.defaults import *
from django.conf import settings

import views.event_bargain
import views.calendar

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    # gigs
    url(r'^gig/new/(?P<band_slug>[-\w]+)/$', views.calendar.gig_create, name='gig-new'),
    url(r'^gig/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', views.calendar.gig_detail, name='gig-detail'),

    url(r'^gig/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/cancel$', views.calendar.gig_cancel, name='gig-cancel'),
    url(r'^gig/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/uncancel$', views.calendar.gig_uncancel, name='gig-uncancel'),

    # Band calendar 
    url(r'^calendar/band/(?P<band_slug>[-\w]+).ics$', views.calendar.band_calendar_ics, name='band-calendar-ics'),
    url(r'^calendar/band/(?P<band_slug>[-\w]+)$', views.calendar.band_calendar_detail, name='band-calendar'),

    # Venue calendar
    url(r'^calendar/venue/(?P<venue_slug>[-\w]+).ics$', views.calendar.venue_calendar_ics, name='venue-calendar-ics'),
    url(r'^calendar/venue/(?P<venue_slug>[-\w]+)$', views.calendar.venue_calendar_detail, name='venue-calendar'),


    # Bargain
    url(r'^bargain/new/(?P<venue_slug>[-\w]+)/$', views.event_bargain.event_bargain_new, name='bargain-new'),

    # Bargain, band specific
    url(r'^bargain/(?P<contract_id>\d+)/band/(?P<band_slug>[-\w]+)/approve$', views.event_bargain.event_bargain_approve_band, name='bargain-approve-band'),
    url(r'^bargain/(?P<contract_id>\d+)/band/(?P<band_slug>[-\w]+)/disapprove$', views.event_bargain.event_bargain_disapprove_band, name='bargain-disapprove-band'),
    url(r'^bargain/(?P<contract_id>\d+)/band/(?P<band_slug>[-\w]+)/update$', views.event_bargain.event_bargain_update_band, name='bargain-update-band'),

    # Bargain, venue specific
    url(r'^bargain/(?P<contract_id>\d+)/venue/(?P<venue_slug>[-\w]+)/approve$', views.event_bargain.event_bargain_approve_venue, name='bargain-approve-venue'),
    url(r'^bargain/(?P<contract_id>\d+)/venue/(?P<venue_slug>[-\w]+)/disapprove$', views.event_bargain.event_bargain_disapprove_venue, name='bargain-disapprove-venue'),
    url(r'^bargain/(?P<contract_id>\d+)/venue/(?P<venue_slug>[-\w]+)/update$', views.event_bargain.event_bargain_update_venue, name='bargain-update-venue'),


    url(r'^bargain/(?P<contract_id>\d+)/detail$', views.event_bargain.event_bargain_detail, name='bargain-detail'),
)


