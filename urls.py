from django.conf.urls.defaults import *

from django.contrib.gis import admin

import authority

import settings

admin.autodiscover()
authority.autodiscover()

urlpatterns = patterns('',
    # temporary index page
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    # auth + profile
    (r'^account/', include('socialregistration.urls')),
    (r'^account/reg/classical/', include('registration.backends.default.urls')),
    (r'^account/', include('account.urls', namespace='account')),

    # comments
    (r'^comments/', include('django.contrib.comments.urls')),

    # Feedback
    (r'^feedback/', include('backcap.urls', namespace='backcap')),

    # Bands
    (r'^bands/', include('band.urls', namespace='band')),
    (r'^bands/', include('album.urls', namespace='album')),

    # Venues
    (r'^venue/', include('venue.urls', namespace='venue')),

    # bargain
    (r'^bargain/', include('bargain.urls', namespace='bargain')),

    # BigBrother
    (r'^bb/', include('bigbrother.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

