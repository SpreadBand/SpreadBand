from django.conf.urls.defaults import *

from django.contrib.gis import admin

import authority

admin.autodiscover()
authority.autodiscover()

urlpatterns = patterns('',
    # temporary index page
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
                       
    # users
    (r'^accounts/', include('registration.backends.default.urls')),

    # Bands
    (r'^bands/', include('bands.urls')),
    # Gigplaces
    (r'^places/', include('gigplaces.urls')),

    (r'^bb/', include('bigbrother.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)
