from django.conf.urls.defaults import *

from django.contrib.gis import admin

import authority

admin.autodiscover()
authority.autodiscover()


urlpatterns = patterns('',
    # Bands
    (r'^bands/', include('bands.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)
