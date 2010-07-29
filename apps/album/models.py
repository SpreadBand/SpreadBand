from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, FileField, ForeignKey, ImageField, BooleanField, OneToOneField, IntegerField, TextField

from imagekit.models import ImageModel
from tagging.fields import TagField

from band.models import Band

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

    description = TextField()

    is_public = BooleanField(help_text=_('If the album is visible by visitors'))

    style_tags = TagField()

    @models.permalink
    def get_absolute_url(self):
        return ('album:detail', (), {'band_slug': self.band.slug, 'album_slug': self.slug})

    def __unicode__(self):
        return '%s - %s' % (self.band.name,
                            self.name)


def get_cover_path(anAlbumCover, filename):
    print "cover=", anAlbumCover
    print "filename=", filename

    dst = 'bands/%d/albums/%d/covers/front/%s' % (anAlbumCover.album.band_id,
                                                  anAlbumCover.album_id,
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
    album = ForeignKey(Album, related_name='cover')

    def __unicode__(self):
        return "Cover for %s" % self.album


from media.models import Track

class AlbumTrack(Track):
    @staticmethod
    def get_track_path(aTrack, filename):
        return 'bands/%d/albums/%d/tracks/%s' % (aTrack.album.band_id,
                                                 aTrack.album_id,
                                                 filename)

    no = IntegerField(blank=True, default=0)
    album = ForeignKey(Album, related_name='tracks')

