from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.db.models import DateField, TimeField, CharField, PositiveSmallIntegerField
from django.db.models import ManyToManyField, ForeignKey, OneToOneField, DateTimeField, TextField
from django.utils.translation import ugettext
_ = lambda u: unicode(ugettext(u))

from django_extensions.db.fields import UUIDField
from timedelta.fields import TimedeltaField
import reversion

# XXX Hack to make south happy with fsmfield
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django_fsm\.db\.fields\.fsmfield\.FSMField"])
# add_introspection_rules([], ["^durationfield\.db\.models\.fields\.duration\.TimeDeField"])

from django_fsm.db.fields import FSMField, transition
import notification.models as notification

from band.models import Band
from venue.models import Venue
from event.models import Gig

from .signals import gigbargain_concluded, gigbargain_new_from_venue

class GigBargainManager(models.Manager):
    """
    Objects manager for GigBargain
    """

    # XXX I think this is fucking slow
    def invitationsFor(self, aBand):
        return self.filter(gigbargainband__in=GigBargainBand.objects.filter(state='waiting', band=aBand))

    def draftsFor(self, aBand):
        return self.filter(state__in=('draft',
                                      'draft_ok')
                           ).exclude(gigbargainband__in=GigBargainBand.objects.filter(state='waiting', band=aBand))

    def new_gigbargains(self):
        return self.filter(state__in=('draft',
                                      'draft_ok',
                                      'new',
                                      'need_venue_confirm'
                                      )
                           )

    def inprogress_gigbargains(self):
        return self.filter(state__in=('complete_proposed_to_venue',
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
        ('new', _('New bargain')),
        ('draft', _('A draft, not proposed to a venue')),
        ('draft_ok', _('A draft, approved by bands')),
        ('complete_proposed_to_venue', _('Complete draft bargain proposed to venue')),
        ('incomplete_proposed_to_venue', _('Incomplete draft bargain proposed to venue')),
        ('need_venue_confirm', _('Need venue confirmation')),
        ('band_nego', _('Bands negociating')),
        ('band_ok', _('Approved by bands')),
        ('concluded', _('Concluded')),
        ('declined', _('Declined')),
        ('canceled', _('Canceled by the initiator'))
        )

    @property
    def macro_state(self):
        if self.state in ('new', 'draft', 'draft_ok'):
            return 'draft'

        elif self.state in ('complete_proposed_to_venue', 'incomplete_proposed_to_venue', 'need_venue_confirm'):
            return 'submitted'

        elif self.state in ('band_nego', 'band_ok'):
            return 'negociations'

        else:
            return 'finished'

    # XXX: Pgsql seems to support native uuid field. This extension may not use that.
    uuid = UUIDField(unique=True, db_index=True, auto=True)

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


    date = DateField(verbose_name=_('Date'))
    opens_at = TimeField(verbose_name=_('Opens at'),
                         null=True, blank=True)
    closes_at = TimeField(verbose_name=_('Closes at'),
                          null=True, blank=True)

    name = CharField(verbose_name=_('Name'),
                     max_length=255,
                     null=True, blank=True,
                     help_text=_('Name of the event'),
                     )

    bands = ManyToManyField(Band, through='GigBargainBand', related_name='gigbargains')

    venue = ForeignKey(Venue, 
                       verbose_name=_('Venue'),
                       related_name='gigbargains')
    venue_reason = TextField(blank=True, null=True)

    ACCESS_CHOICES = [
        ('FREE', _('Free Access')),
        ('FEES', _('Entrance Fee')),
        ('DRNK', _('Drink')),
        ('TICK', _('Ticket')),
        ]
    access = CharField(verbose_name=_('Access type'),
                       max_length=4, choices=ACCESS_CHOICES)
    fee_amount = PositiveSmallIntegerField(verbose_name=_('Fee amount'),
                                           null=True, blank=True)

    REMUNERATION_CHOICES = [
        ('NONE', _('No remuneration')),
        ('FIXE', _('Fixed Amount')),
        ('PERC', _('Percentage')),
        ]
    remuneration = CharField(verbose_name=_('artist remuneration type'),
                             max_length=4, choices=REMUNERATION_CHOICES, 
                             null=True, blank=True,
                             help_text=_("How earned money will be dispatched to artists"))

    gig = OneToOneField(Gig, null=True, 
                        related_name='gigbargain', 
                        editable=False, 
                        help_text=_("The produced gig"))
                             
    def save(self, *args, **kwargs):
        # Auto create VenueState when creating this model
        # if not self.pk:
        #    self.venue_state = GigBargainVenueState.objects.create()

        return models.Model.save(self, *args, **kwargs)


    def name_or_default(self):
        """
        Return the title of the gig bargain or a generic one 
        """
        if self.name:
            return self.name
        else:
            return "Gig Bagain at %s" % (self.venue.name)

    def __unicode__(self):
        text = self.name_or_default()
        if self.state == 'concluded':
            text += ' (concluded)'
        else:
            text += ' (in progress)'

        return text

    @models.permalink
    def get_absolute_url(self):
        return ('gigbargain:gigbargain-detail', (self.uuid,))


class GigBargainBandManager(models.Manager):
    """
    Objects manager for GigBargainBand
    """
    def concurring(self):
        """
        Return bands that are still concurring for this bargain
        """
        return self.filter(state__in=('waiting', 'accepted', 'negociating', 'part_validated'))

    def not_concurring(self):
        """
        Returns the bands that are no more concurring
        """
        return self.exclude(state__in=('waiting', 'accepted', 'negociating', 'part_validated'))        
    
class GigBargainBand(models.Model):
    """
    Data related to a gig bargain for a given band 
    """
    class Meta:
        ordering = ('band__name',)

    objects = GigBargainBandManager()

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


    band = ForeignKey(Band,
                      verbose_name=_('Band'),
                      related_name='gigbargainbands')

    bargain = ForeignKey(GigBargain)

    joined_on = DateTimeField(auto_now_add=True)

    reason = TextField(blank=True, null=True)

    starts_at = TimeField(verbose_name=_('Starts at'),
                          help_text=_("e.g. 20:30 or 10:15"),
                          blank=True, null=True, 
                          )

    set_duration = TimedeltaField(verbose_name=_('Set duration'),
                                  blank=True, null=True,
                                  help_text=_("as a duration. e.g. '4 hours, 2 minutes'")
                                  )

    eq_starts_at = TimeField(verbose_name=_('Equalisation starts at'),
                             blank=True, null=True)
    
    percentage = PositiveSmallIntegerField(verbose_name=_('Percentage'),
                                           blank=True, null=True, default=0)
    amount = PositiveSmallIntegerField(verbose_name=_('Amount'),
                                       blank=True, null=True, default=0)
    defrayment = PositiveSmallIntegerField(verbose_name=_('Defrayment'),
                                           blank=True, null=True, default=0)

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
        return ('gigbargain:gigbargain-band-part-display', (self.bargain_id, self.band.slug))

## Reversion
if not reversion.is_registered(GigBargain):
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
from event.models import Gig

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
              description=_('no description'),
              title=_("gig at %s") % gigbargain.venue.name,
              slug="gig-%s" % gigbargain.venue.slug)

    gig.save()

    # Add all participating bands to the gig event
    for band in gigbargain.gigbargainband_set.concurring():
        gig.bands.add(band.band)

    # Add this gig to the band calendars
    for band in gigbargain.gigbargainband_set.concurring():
        band.band.calendar.events.add(gig)

    # Also add this gig to the venue calendar            
    gig.venue.calendar.events.add(gig)
    
    # Attach the gig to the bargain
    gigbargain.gig = gig
    gigbargain.save()


# FIXME: This is suboptimal
def collect_band_members_from_gigbargain(aGigBargain):
    """
    Collect users from bands to send notification to
    """
    users = set()
    for gigbargainband in aGigBargain.gigbargainband_set.concurring():
        for member in gigbargainband.band.members.all():
            users.add(member)

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

