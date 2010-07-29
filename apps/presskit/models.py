from django.db import models

from django.db.models import ForeignKey, ManyToManyField, OneToOneField

from band.models import Band
from media.models import Track

class PressKit(models.Model):
    tracks = ManyToManyField(Track, blank=True)
    band = OneToOneField(Band, related_name='presskit')

    def __unicode__(self):
        return "PressKit for %s" % self.band.name

    
