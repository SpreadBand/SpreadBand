from django.conf.urls.defaults import *

from django.contrib.gis import admin

import authority

import settings

admin.autodiscover()
authority.autodiscover()

# Sitemaps
import venue.sitemaps
import band.sitemaps
import event.sitemaps
sitemaps = {}
sitemaps.update(venue.sitemaps.sitemaps)
sitemaps.update(band.sitemaps.sitemaps)
sitemaps.update(event.sitemaps.sitemaps)

# URLS
urlpatterns = patterns('',
    # temporary index page
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}, name='home'),

    # auth + profile
    (r'^user/', include('socialregistration.urls')),
    (r'^user/', include('account.urls', namespace='account')),

    # comments
    (r'^comments/', include('django.contrib.comments.urls')),

    # reviews
    (r'^reviews/', include('reviews.urls')),

    # Feedback
    (r'^feedback/', include('backcap.urls', namespace='backcap')),

    # Bands
    (r'^b/', include('band.urls', namespace='band')),
    (r'^b/', include('album.urls', namespace='album')),
    (r'^b/', include('presskit.urls', namespace='presskit')),

    # Venues
    (r'^v/', include('venue.urls', namespace='venue')),

    # Events
    (r'^e/', include('event.urls', namespace='event')),

    # bargain
    (r'^e/gigbargain/', include('gigbargain.urls', namespace='gigbargain')),

    # BigBrother
    (r'^bb/', include('bigbrother.urls')),

    # Ajax select channels
    (r'^ajax_select/', include('ajax_select.urls')),

    # Activity stream
    (r'^activity/', include('actstream.urls')),

    # Notifications
    (r'^notification/', include('notification.urls')),

    # Search
    (r'^search/', include('haystack.urls')),

    # REST API
    (r'^api/', include('api.urls')),

    # Robots.txt and sitemap
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots\.txt$', include('robots.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

