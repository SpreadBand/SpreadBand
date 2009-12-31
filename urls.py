from django.conf.urls.defaults import *

from django.contrib.gis import admin

import authority

admin.autodiscover()
authority.autodiscover()

urlpatterns = patterns('',
    # users
    (r'^accounts/', include('registration.backends.default.urls')),

    # Bands
    (r'^bands/', include('bands.urls')),
    # Gigplaces
    (r'^places/', include('gigplaces.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)
