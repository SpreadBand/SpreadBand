from django.conf.urls.defaults import url, patterns
from django.conf import settings

import views.bargain.band
import views.bargain.venue


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
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)$', views.bargain.gigbargain_detail, name='gigbargain-detail'),

    # Bargain, comments
    url(r'bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/comments/(?P<section>[-\w]+)$', views.bargain.comments_section_display, name='gigbargain-comments-section-display'),

    # Bargain, venue specific
    url(r'^bargain/gig/new/venue$', views.bargain.venue.gigbargain_new_from_venue, name='gigbargain-new-from-venue'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/venue/confirm_bands$', views.bargain.venue.gigbargain_venue_confirm_bands, name='gigbargain-venue-confirm-bands'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/venue/conclude$', views.bargain.venue.gigbargain_venue_conclude, name='gigbargain-venue-conclude'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/venue/decline$', views.bargain.venue.gigbargain_venue_decline, name='gigbargain-venue-decline'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/venue/enter$', views.bargain.venue.gigbargain_venue_enter_negociations, name='gigbargain-venue-enter'),

    # Bargain, band specific
    url(r'^bargain/gig/new/band/(?P<band_slug>[-\w]+)$', views.bargain.band.gigbargain_new_from_band, name='gigbargain-new-from-band'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/enter$', views.bargain.band.gigbargain_enter_for_band, name='gigbargain-enter-for-band'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/reject$', views.bargain.band.gigbargain_refuse_for_band, name='gigbargain-refuse-for-band'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/quit$', views.bargain.band.gigbargain_band_quit, name='gigbargain-band-quit'),

    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/approve$', views.bargain.band.gigbargain_band_part_approve, name='gigbargain-band-part-approve'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/edit$', views.bargain.band.gigbargain_band_part_edit, name='gigbargain-band-part-edit'),

    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)$', views.bargain.band.gigbargain_band_part_display, name='gigbargain-band-part-display'),

    # Bargain, common parts
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/common/band/(?P<band_slug>[-\w]+)$', views.bargain.band.gigbargain_band_common_edit, name='gigbargain-band-common-edit'),
    url(r'^bargain/gig/(?P<gigbargain_uuid>[\w\d-]+)/common/venue$', views.bargain.venue.gigbargain_venue_common_edit, name='gigbargain-venue-common-edit'),


)


