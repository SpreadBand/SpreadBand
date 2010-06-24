from django.db import models
from django.db.models import DateField, TimeField, CharField, PositiveSmallIntegerField
from django.db.models import ManyToManyField, ForeignKey

from agenda.models import Event

from band.models import Band
from venue.models import Venue
from bargain.models import Terms
from bargain.signals import contract_concluded

#from agenda.models import EventManager

class Gig(Event):
    """
    A gig related to a Venue and one or more Bands
    """
    # objects = EventManager()

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
    
#-- Bargain

class GigBargain(Terms):
    """
    Terms of a bargain between one or more Bands and a Venue.
    """
    date = DateField()
    opens_at = TimeField()
    closes_at = TimeField()

    bands = ManyToManyField(Band, through='GigBargainBand')
    venue = ForeignKey(Venue)

    ACCESS_CHOICES = (
        ('FREE', 'Free Access'),
        ('FEES', 'Entrance Fee'),
        ('DRNK', 'Drink'),
        ('TICK', 'Ticket'),
        )
    access = CharField(max_length=4, choices=ACCESS_CHOICES)

    fee_amount = PositiveSmallIntegerField(null=True, blank=True)
    
    @staticmethod
    def getForm():
        from django.forms.models import formset_factory
        from .forms import GigBargainForm, GigBargainBandForm
        
        GigBargainBandFormSet = formset_factory(GigBargainBandForm)

        return GigBargainForm, ['bargain', GigBargainBandFormSet]

    def getParticipants(self):
        parties = [b for b in self.bands.all()] + [self.venue]
        return parties

    def __unicode__(self):
        return u'Gig bargain at [%s]' % (self.venue)

    @models.permalink
    def get_absolute_url(self):
        return ('event:bargain-detail', (self.id,))
    
class GigBargainBand(models.Model):
    """
    Data related to a gig bargain for a given band 
    """
    band = ForeignKey(Band)
    bargain = ForeignKey(GigBargain)

    starts_at = TimeField()
    ends_at = TimeField()

    eq_starts_at = TimeField()
    
    REMUNERATION_CHOICES = (
        ('NONE', 'No remuneration'),
        ('FIXE', 'Fixed Amount'),
        ('PERC', 'Percentage'),
        )

    remuneration = CharField(max_length=4, choices=REMUNERATION_CHOICES)

    percentage = PositiveSmallIntegerField(blank=True, null=True, default=None)
    amount = PositiveSmallIntegerField(blank=True, null=True, default=None)
    
    def __unicode__(self):
        return u'%s' % self.band
    

## Signals
from bargain.signals import contract_new

def gigbargain_concluded_callback(sender, aContract, aUser, **kwargs):
    """
    Callback when a gig bargain has been concluded
    """
    gigbargain = aContract.terms.gigbargain

    gig = Gig(venue_id=gigbargain.venue.id,
              event_date=gigbargain.date,
              start_time=gigbargain.opens_at,
              end_time=gigbargain.closes_at,
              description='no description',
              title="gig at %s" % gigbargain.venue.name,
              slug="gig-at-%s" % gigbargain.venue.slug,
              author=aUser)

    gig.save()

    # Add all participating bands to the gig event
    for band in gigbargain.bands.all():
        gig.bands.add(band)

    # Add this gig to the band calendars
    for band in gigbargain.bands.all():
        band.calendar.events.add(gig)

    # Also add this gig to the venue calendar            
    gig.venue.calendar.events.add(gig)

    
contract_concluded.connect(gigbargain_concluded_callback, sender=GigBargain)

import notification.models as notification

# FIXME: This is suboptimal and people can get notified many times if they are in multiple bands
def gigbargain_new_callback(sender, aContract, **kwargs):
    terms = aContract.terms.gigbargain

    # Collect users from bands to send notification to
    users = []
    for band in terms.bands.all():
        for member in band.members.all():
            users.append(member.user)
    
    notification.send(users, 'new_gig_bargain')

contract_new.connect(gigbargain_new_callback, sender=GigBargain)
