from django.db import models
from django.db.models import ManyToManyField, ForeignKey
from django.utils.translation import ugettext
_ = lambda u: unicode(ugettext(u))

from agenda.models import Event

from apps.band.models import Band
from venue.models import Venue

class Gig(Event):
    """
    A gig related to a Venue and one or more Bands
    """
    venue = ForeignKey(Venue, 
                       verbose_name=_('Venue'),
                       related_name='gigs')

    bands = ManyToManyField(Band, 
                            verbose_name=_('Bands'),
                            related_name='gigs')

    @models.permalink                                               
    def get_absolute_url(self):
        return ('event:gig-detail', 
                (),
                {'year'  : self.event_date.year, 
                 'month' : self.event_date.month, 
                 'day'   : self.event_date.day, 
                 'slug'  : self.slug }
                )
    
