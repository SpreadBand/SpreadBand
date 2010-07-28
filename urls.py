from django.conf.urls.defaults import *

from django.contrib.gis import admin

import authority

import settings

admin.autodiscover()
authority.autodiscover()

urlpatterns = patterns('',
    # temporary index page
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}, name='home'),

    # auth + profile
    (r'^user/', include('socialregistration.urls')),
    (r'^user/reg/classical/', include('registration.backends.default.urls')),
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

    # REST API
    (r'^api/', include('api.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

