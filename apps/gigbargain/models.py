from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.db.models import DateField, TimeField, CharField, PositiveSmallIntegerField
from django.db.models import ManyToManyField, ForeignKey, OneToOneField
from django.utils.translation import ugettext as _

from django_extensions.db.fields import UUIDField
from timedelta.fields import TimedeltaField
import reversion

# XXX Hack to make south happy with fsmfield
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django_fsm\.db\.fields\.fsmfield\.FSMField"])
# add_introspection_rules([], ["^durationfield\.db\.models\.fields\.duration\.TimeDeField"])

from agenda.models import Event
from django_fsm.db.fields import FSMField, transition
import notification.models as notification

from band.models import Band
from venue.models import Venue

from .signals import gigbargain_concluded, gigbargain_new_from_venue

class GigBargainManager(models.Manager):
    """
    Objects manager for GigBargain
    """
    def new_gigbargains(self):
        return self.filter(state__in=('new',
                                      'need_venue_confirm'
                                      )
                           )

    def inprogress_gigbargains(self):
        return self.filter(state__in=('draft',
                                      'draft_ok',
                                      'complete_proposed_to_venue',
                                      'incomplete_proposed_to_venue',
                                      'band_nego',
                                      'band_ok'
                                      )
                           )

    def concluded_gigbargains(self):
        return self.filter(state='concluded')

class GigBargain(models.Model):
    """
    Terms of a bargain between one or more Bands and a Venue.
    """
    objects = GigBargainManager()

    STATE_CHOICES = (
        ('new', 'New bargain'),
        ('draft', 'A draft, not proposed to a venue'),
        ('draft_ok', 'A draft, approved by bands'),
        ('complete_proposed_to_venue', 'Complete draft bargain proposed to venue'),
        ('incomplete_proposed_to_venue', 'Incomplete draft bargain proposed to venue'),
        ('need_venue_confirm', 'Need venue confirmation'),
        ('band_nego', 'Bands negociating'),
        ('band_ok', 'Approved by bands'),
        ('concluded', 'Concluded'),
        ('declined', 'Declined'),
        ('canceled', 'Canceled by the initiator')
        )

    # XXX: Pgsql seems to support native uuid field. This extension may not use that.
    uuid = UUIDField(primary_key=True, db_index=True, auto=True)

    #-- State management
    state = FSMField(default='new')

    @transition(source=('new', 'need_venue_confirm'), target='band_nego', save=True)
    def start_band_negociation(self):
        """
        Start negociation between bands.
        """
        for gigbargainband in self.gigbargainband_set.filter(state='accepted'):
            gigbargainband.start_negociating()

    @transition(source='new', target='incomplete_proposed_to_venue', save=True)
    def propose_incomplete_bargain_to_venue(self):
        """
        Propose this incomplete bargain to the venue (used when initiated from band)
        """
        pass

    @transition(source=('new', 'draft_ok'), target='complete_proposed_to_venue', save=True)
    def propose_complete_bargain_to_venue(self):
        """
        Propose this complete bargain to the venue (used when initiated from band)
        """
        pass

    @transition(source='new', target='need_venue_confirm', save=True)
    def need_venue_confirmation(self):
        """
        When only /some/ of the bands have accepted to enter the bargain
        """
        pass

    @transition(source=('incomplete_proposed_to_venue', 'complete_proposed_to_venue'), target='band_nego', save=True)
    def venue_enter_negociations(self):
        """
        When a venue accepts to enter negociations with bands.
        """
        pass

    @transition(source=('band_nego', 'band_ok'), target='band_ok', save=True)
    def bands_have_approved_parts(self):
        """
        When all bands have approved their parts
        """
        pass

    @transition(source=('band_nego', 'band_ok'), target='band_nego', save=True)
    def bands_dont_agree_anymore(self):
        """
        When at least one of the bands don't agree anymore
        """
        pass

    @transition(source='draft', target='draft_ok', save=True)
    def bands_have_approved_draft(self):
        """
        When all bands have validated their parts during a draft
        """
        pass

    @transition(source='draft_ok', target='draft', save=True)
    def bands_have_disapproved_draft(self):
        """
        When we need to reset a draft (something is wrong with the draft)
        """
        pass

    @transition(source=('band_ok', 'complete_proposed_to_venue'), target='concluded', save=True)
    def conclude(self):
        """
        Conclude the bargain
        """
        gigbargain_concluded.send(sender=self)

    @transition(source=('band_ok', 'complete_proposed_to_venue', 'incomplete_proposed_to_venue'), target='declined', save=True)
    def decline(self):
        """
        Decline the bargain
        """
        pass

    @transition(source='need_venue_confirm', target='canceled', save=True)
    def cancel(self):
        """
        Cancel the bargain
        """
        pass


    @transition(source='new', target='draft', save=True)
    def become_draft(self):
        """
        Make this gig bargain becomes a draft.
        """
        pass


    date = DateField()
    opens_at = TimeField(null=True, blank=True)
    closes_at = TimeField(null=True, blank=True)

    name = CharField(max_length=255,
                     null=True, blank=True,
                     help_text=_('Name of the event'),
                     )

    bands = ManyToManyField(Band, through='GigBargainBand', related_name='gigbargains')

    venue = ForeignKey(Venue, related_name='gigbargains')
    # venue_state = OneToOneField(GigBargainVenueState, related_name='gigbargain')

    ACCESS_CHOICES = [
        ('FREE', 'Free Access'),
        ('FEES', 'Entrance Fee'),
        ('DRNK', 'Drink'),
        ('TICK', 'Ticket'),
        ]
    access = CharField(max_length=4, choices=ACCESS_CHOICES)
    fee_amount = PositiveSmallIntegerField(null=True, blank=True)

    REMUNERATION_CHOICES = [
        ('NONE', 'No remuneration'),
        ('FIXE', 'Fixed Amount'),
        ('PERC', 'Percentage'),
        ]
    remuneration = CharField(max_length=4, choices=REMUNERATION_CHOICES, 
                             null=True, blank=True,
                             help_text=_("How earned money will be dispatched "))
                             

    def save(self, *args, **kwargs):
        # Auto create VenueState when creating this model
        # if not self.pk:
        #    self.venue_state = GigBargainVenueState.objects.create()

        models.Model.save(self, *args, **kwargs)

    def __unicode__(self):
        text = u'Gig bargain at [%s] with [%s] on %s' % (self.venue,
                                                         [b.name for b in self.bands.all()],
                                                         self.date)
        if self.state == 'concluded':
            text += ' (concluded)'
        else:
            text += ' (in progress)'

        return text

    @models.permalink
    def get_absolute_url(self):
        return ('event:gigbargain-detail', (self.uuid,))

    
class GigBargainBand(models.Model):
    """
    Data related to a gig bargain for a given band 
    """
    STATE_CHOICES = (
        ('waiting', 'Waiting for reply'),
        ('accepted', 'Bargain accepted'),
        ('negociating', 'Negociating with others bands'),

        ('part_validated', 'The band has validated its part'),

        ('refused', 'Bargain refused'),
        ('exited', 'Left bargain'),
        ('kicked', 'Kicked from bargain'),
        )

    #-- State management
    state = FSMField(default='waiting')

    @transition(source='waiting', target='accepted', save=True)
    def accept(self):
        pass

    @transition(source='waiting', target='refused', save=True)
    def refuse(self):
        pass

    @transition(source='accepted', target='negociating', save=True)
    def start_negociating(self):
        pass

    @transition(source=('negociating', 'part_validated'), target='part_validated', save=True)
    def approve_part(self):
        """
        When a band approves its part of the contract
        """
        pass

    @transition(source='part_validated', target='negociating', save=True)
    def cancel_approval(self):
        """
        Cancels the approval of the band's part
        """
        pass

    @transition(source='negociating', target='kicked', save=True)
    def kick(self):
        """
        Kicks a band
        """
        pass


    band = ForeignKey(Band)
    bargain = ForeignKey(GigBargain)

    starts_at = TimeField(blank=True, null=True)
    set_duration = TimedeltaField()

    eq_starts_at = TimeField(blank=True, null=True)
    
    percentage = PositiveSmallIntegerField(blank=True, null=True, default=0)
    amount = PositiveSmallIntegerField(blank=True, null=True, default=0)
    defrayment = PositiveSmallIntegerField(blank=True, null=True, default=0)

    def clean(self):
        # Make sure percentages of all bands don't exceed 100
        # XXX: We have to filter out bands that have left the bargain
        # other_percentage = GigBargainBand.objects.filter(bargain=self.bargain).exclude(pk=self.pk).aggregate(Sum("percentage"))['percentage__sum']
        # if (other_percentage or 0) + (self.percentage or 0) > 100:
        #    raise ValidationError(_("The sum of all band's percentages exceeds 100, please reduce yours."))

        return models.Model.clean(self)
    
    def __unicode__(self):
        return u'%s' % self.band

    @models.permalink
    def get_absolute_url(self):
        return ('event:gigbargain-band-part-display', (self.bargain_id, self.band.slug))

## Reversion
reversion.register(GigBargain, follow=['bargainbands', 'venue_state'])
reversion.register(GigBargainBand)

class GigBargainCommentThread(models.Model):
    """
    A comment thread about a specific part of a GigBargain
    """
    class Meta:
        unique_together = (('id', 'section'))

    section = CharField(max_length=50, db_index=True)
    gigbargain = ForeignKey(GigBargain, related_name='comment_threads')


## Signals
from annoying.decorators import signals

@signals(gigbargain_concluded)
def gigbargain_concluded_callback(sender, **kwargs):
    """
    Callback when a gig bargain has been concluded
    """
    gigbargain = sender

    gig = Gig(venue_id=gigbargain.venue.id,
              event_date=gigbargain.date,
              start_time=gigbargain.opens_at,
              end_time=gigbargain.closes_at,
              description='no description',
              title="gig at %s" % gigbargain.venue.name,
              slug="gig-at-%s" % gigbargain.venue.slug)

    gig.save()

    # Add all participating bands to the gig event
    for band in gigbargain.bands.all():
        gig.bands.add(band)

    # Add this gig to the band calendars
    for band in gigbargain.bands.all():
        band.calendar.events.add(gig)

    # Also add this gig to the venue calendar            
    gig.venue.calendar.events.add(gig)


# FIXME: This is suboptimal
def collect_band_members_from_gigbargain(aGigBargain):
    """
    Collect users from bands to send notification to
    """
    users = set()
    for band in aGigBargain.bands.all():
        for member in band.members.all():
            users.add(member.user)

    return users
    
@signals(gigbargain_new_from_venue)
def gigbargain_new_from_venue_callback(sender, aGigBargain, **kwargs):
    users = collect_band_members_from_gigbargain(aGigBargain)
    notification.send(users, 'gigbargain_new')


def gigbargain_approved_callback(sender, aContract, aParticipant,  **kwargs):
    users = collect_band_members_from_gigbargain(aContract)
    notification.send(users, 'gigbargain_approved')


def gigbargain_disapproved_callback(sender, aContract, aParticipant,  **kwargs):
    users = collect_band_members_from_gigbargain(aContract)
    notification.send(users, 'gigbargain_disapproved')


def gigbargain_amended_callback(sender, aContract, aParticipant,  **kwargs):
    users = collect_band_members_from_gigbargain(aContract)
    notification.send(users, 'gigbargain_amended')

