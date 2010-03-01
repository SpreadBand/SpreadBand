from django.conf.urls.defaults import *

from django.contrib.gis import admin

import authority

import settings

admin.autodiscover()
authority.autodiscover()

urlpatterns = patterns('',
    # temporary index page
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    # users
    (r'^accounts/', include('registration.backends.default.urls')),

    # Bands
    (r'^bands/', include('bands.urls', namespace='band')),

    # Gigplaces
    (r'^places/', include('gigplaces.urls')),

    (r'^bb/', include('bigbrother.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

