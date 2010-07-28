from django.db import models
from django.db.models import ManyToManyField, ForeignKey
from django.utils.translation import ugettext as _

from agenda.models import Event

from band.models import Band
from event.signals import gigbargain_concluded
from venue.models import Venue

class Gig(Event):
    """
    A gig related to a Venue and one or more Bands
    """
    venue = ForeignKey(Venue, related_name='gigs')
    bands = ManyToManyField(Band, related_name='gigs')

    @models.permalink                                               
    def get_absolute_url(self):
        return ('event:gig-detail', 
                (),
                {'year'  : self.event_date.year, 
                 'month' : self.event_date.month, 
                 'day'   : self.event_date.day, 
                 'slug'  : self.slug }
                )
    
