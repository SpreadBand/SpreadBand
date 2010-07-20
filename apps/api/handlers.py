from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended

from event.models import Gig

class CalendarHandler(BaseHandler):
    """
    Authenticated entrypoint for Calendars.
    """
    allowed_methods = ('GET',)
    model = Gig
    fields = (('venue', ('name',)),
              'title',
              'event_date',
              ('bands', ('name',)))

    def read(self, request, venue_slug):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.
        
        Parameters:
         - `venue_slug`: The slug of the venue to retrieve.
        """
        base = Gig.objects.future_events()
        
        return base.get(venue__slug=venue_slug)


