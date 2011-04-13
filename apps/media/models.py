from mutagen.easyid3 import EasyID3

import uuid
import os

from django.db import models
from django.db.models import IntegerField, CharField, FileField


class Track(models.Model):
    @staticmethod
    def get_track_path(aTrack, filename):
        """
        Generate a random UUID for a track,
        create a two-level directory depth (so that it is indexed by the FS),
        use the uuid as the track name
        """
        track_uuid = uuid.uuid4()
        lev1 = track_uuid.hex[0:8]
        lev2 = track_uuid.hex[8:12]
        name, extension = os.path.splitext(filename)
        return 'tracks/%s/%s/%s%s' % (lev1, lev2, track_uuid, extension)

    title = CharField(max_length=255, default='Unnamed', blank=True)
    file = FileField(upload_to=lambda instance, name: instance.get_track_path(instance, name))

    def __unicode__(self):
        return '%s' % (self.title)
