from django.db import models

from django.utils.translation import ugettext
_ = lambda u: unicode(ugettext(u))

from django.contrib.auth.models import User
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.db.models import URLField
from django.db.models.signals import post_save

from badges.models import Badge

from band.models import Band
from venue.models import Venue
from media.models import Track

class PressKit(models.Model):
    band = OneToOneField(Band, related_name='presskit')

    tracks = ManyToManyField(Track, blank=True)
    video = URLField(max_length=500, 
                     blank=True, null=True)

    def __unicode__(self):
        return "PressKit for %s" % self.band.name

    @models.permalink
    def get_absolute_url(self):
        return ('presskit:presskit-detail', 
                (),
                {'band_slug': self.band.slug}
                )


class PresskitViewRequest(models.Model):
    state_choices = (('P', _("Pending")),
                     ('S', _("Seen")),
                     ('A', _("Accepted")),
                     ('D', _("Declined")),
                     ('C', _("Canceled"))
                     )

    sent_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True,
                                       auto_now_add=True)
    sent_by = models.ForeignKey(User)

    presskit = models.ForeignKey(PressKit)
    venue = models.ForeignKey(Venue)

    seen = models.BooleanField(default=False)

    state = models.CharField(max_length=1,
                             choices=state_choices,
                             default='P')

    def __unicode__(self):
        return "Request of %s for %s (%s)" % (self.presskit.band.name,
                                              self.venue.name,
                                              self.get_state_display())


def create_presskit_for_band(sender, instance, created, **kwargs):
    """
    Called to ensure the presskit is created when a band is instanciated
    """
    if created:
        presskit = PressKit(band=instance)
        presskit.save()

post_save.connect(create_presskit_for_band, sender=Band)

def check_for_awards(sender, instance, created, **kwargs):
    """
    Check if we triggers an award such as presskit completion
    """
    if not created:
        presskit_completion = Badge.objects.get(id='presskitcompletion')
        presskit_completion.meta_badge.award_ceremony(instance.band)

post_save.connect(check_for_awards, sender=PressKit)

