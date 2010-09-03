from django.db import models

from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.db.models import URLField
from django.db.models.signals import post_save

from band.models import Band
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


def create_presskit_for_band(sender, instance, created, **kwargs):
    """
    Called to ensure the presskit is created when a band is instanciated
    """
    if created:
        presskit = PressKit(band=instance)
        presskit.save()

post_save.connect(create_presskit_for_band, sender=Band)
