from django.conf.urls.defaults import *

from django.contrib import admin
import authority

admin.autodiscover()
authority.autodiscover()


urlpatterns = patterns('',
    # Example:
    #(r'^myapp/', include('booking.apps.myapp.urls')),
    (r'^', include(admin.site.urls)),
)
