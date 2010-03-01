import os

from django.db import models
from django.db.models import CharField, FileField, ForeignKey

from bands.models import Band

class Album(models.Model):
    band = ForeignKey(Band, related_name='albums')
    name = CharField(max_length=100)

    @models.permalink
    def get_absolute_url(self):
        # return ('band:album:detail', (), {'album_id': self.id})
        # XXX: hardcoded
        return '/bands/%d/album/%d' % (self.band.id, self.id)

    def __unicode__(self):
        return '%s - %s' % (self.band.name,
                            self.name)

def get_track_path(aTrack, filename):
    return 'bands/%d/albums/%d/%s' % (aTrack.album.band.id,
                                      aTrack.album.id,
                                      filename)

class Track(models.Model):
    album = ForeignKey(Album, related_name='tracks')
    title = CharField(max_length=255)
    file = FileField(upload_to=get_track_path)

    def __unicode__(self):
        return '%s - %s - %s' % (self.album.band.name,
                                 self.album.name,
                                 self.title)
    
