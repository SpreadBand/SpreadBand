from django.conf.urls.defaults import url, patterns
from django.conf import settings

import views.calendar
import views.archive

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    # gigs
    url(r'^gig/new/(?P<band_slug>[-\w]+)/$', views.calendar.gig_create, name='gig-new'),
    url(r'^gig/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', views.calendar.gig_detail, name='gig-detail'),

    url(r'^gig/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/cancel$', views.calendar.gig_cancel, name='gig-cancel'),
    url(r'^gig/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/uncancel$', views.calendar.gig_uncancel, name='gig-uncancel'),

    # Archive
    url(r'^gigs/today$', views.archive.gigs_today, name='archive-gigs-today'),

    # Band calendar 
    url(r'^calendar/band/(?P<band_slug>[-\w]+).ics$', views.calendar.band_calendar_ics, name='band-calendar-ics'),
    url(r'^calendar/band/(?P<band_slug>[-\w]+)$', views.calendar.band_calendar_detail, name='band-calendar'),

    # Venue calendar
    url(r'^calendar/venue/(?P<venue_slug>[-\w]+).ics$', views.calendar.venue_calendar_ics, name='venue-calendar-ics'),
    url(r'^calendar/venue/(?P<venue_slug>[-\w]+)$', views.calendar.venue_calendar_detail, name='venue-calendar'),

)


