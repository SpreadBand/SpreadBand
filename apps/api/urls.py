from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view

from .handlers import CalendarHandler

auth = HttpBasicAuthentication(realm='SpreadBand API')

calendars = Resource(handler=CalendarHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^calendar/venue/(?P<venue_slug>[-\w]+)/$', calendars),

    # automated documentation
    url(r'^$', documentation_view),
)
