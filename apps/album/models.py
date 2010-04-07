from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, FileField, ForeignKey, ImageField, BooleanField, OneToOneField, IntegerField

from imagekit.models import ImageModel
from tagging.fields import TagField

from bands.models import Band

###-- Album

class Album(models.Model):
    ALBUM_KINDS = (
        ('DM', 'Demo'),
        ('EP', 'Extended-play (EP)'),
        ('LP', 'Long-playing (LP)'),
    )

    band = ForeignKey(Band, related_name='albums')

    name = CharField(max_length=100)
    slug = models.SlugField(max_length=40, unique=True)

    kind = CharField(max_length=2, choices=ALBUM_KINDS, default='LP', blank=True)

    is_public = BooleanField(help_text=_('If the album is visible by visitors'))

    style_tags = TagField()

    @models.permalink
    def get_absolute_url(self):
        return ('album:detail', (), {'band_slug': self.band.slug, 'album_slug': self.slug})

    def __unicode__(self):
        return '%s - %s' % (self.band.name,
                            self.name)

from bigbrother.models import ModelStats, InstanceCount, StatsIndex
from bigbrother.hooks import collect_stats

class AlbumStats(ModelStats):
    class Meta:
        model = Album

    # names = StatsIndex('name')
    count = InstanceCount()
    

collect_stats(AlbumStats)



def get_cover_path(anAlbumCover, filename):
    dst = 'bands/%d/albums/%d/covers/front/%s' % (anAlbumCover.album.band.id,
                                                  anAlbumCover.album.id,
                                                  filename)
    return dst

class AlbumCover(ImageModel):
    """
    An image corresponding to the cover of an album
    """
    class IKOptions:
        image_field = 'original_image'
        spec_module = 'album.imagespecs'

    original_image = models.ImageField(upload_to=get_cover_path)
    album = OneToOneField(Album, primary_key=True)

    def __unicode__(self):
        return "Cover for %s" % self.album



###-- Track

def get_track_path(aTrack, filename):
    return 'bands/%d/albums/%d/tracks/%s' % (aTrack.album.band_id,
                                             aTrack.album_id,
                                             filename)

from mutagen.easyid3 import EasyID3

class Track(models.Model):
    album = ForeignKey(Album, related_name='tracks')
    no = IntegerField(blank=True, default=0)
    title = CharField(max_length=255, default='Unnamed', blank=True)
    file = FileField(upload_to=get_track_path)

    def __unicode__(self):
        return '%s - %s - %s' % (self.album.band.name,
                                 self.album.name,
                                 self.title)
    
    # def save(self, *args, **kwargs):
    #     """
    #     Here, we fill the track fields if there are not yet here.
    #     Then, we regularly save the model to the DB.
    #     """
    #     return models.Model.save(*args, **kwargs)
