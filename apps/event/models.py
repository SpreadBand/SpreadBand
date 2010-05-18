from django.db import models

from django.db.models import DateField, TimeField, CharField, PositiveSmallIntegerField
from django.db.models import ManyToManyField, ForeignKey

from band.models import Band
from venue.models import Venue

from schedule.models import Event

class Gig(Event):
    pass

#-- Bargain
from bargain.models import Terms

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
    