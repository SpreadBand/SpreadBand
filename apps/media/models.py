from mutagen.easyid3 import EasyID3

from django.db import models
from django.db.models import IntegerField, CharField, FileField


class Track(models.Model):
    @staticmethod
    def get_track_path(aTrack, filename):
        return 'tracks/%s' % filename

    title = CharField(max_length=255, default='Unnamed', blank=True)
    file = FileField(upload_to=lambda instance, name: instance.get_track_path(instance, name))

    def __unicode__(self):
        return '%s' % (self.title)
