from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, ManyToManyField, DateField, TextField, ForeignKey, BooleanField
from django.contrib.auth.models import User

from tagging.fields import TagField
from imagekit.models import ImageModel

from actors.models import Actor
from minisite.models.minisite import Minisite

class BandRole(models.Model):
    """
    A typed role in a band. Eg: guitarist
    """
    label = CharField(max_length=30,
                      unique=True)

    def __unicode__(self):
        return self.label


class Band(Actor):
    """
    A music band
    """
    name = CharField(max_length=200)
    
    slug = models.SlugField(max_length=40, unique=True)

    founded_on = DateField(help_text=_('When the band was founded'),
                           blank=True,
                           null=True)
    
    genres = TagField('Genres')

    biography = TextField(blank=True,
                          help_text=_('Band biography'))


    website = ForeignKey(Minisite, blank=True, null=True)
    
    #-- Functions
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('band:detail',  (self.slug,))

# This should be in actors.models, but django currently doesn't deal
# well with signals and inheritance
from django.db.models.signals import post_save
from actors.models import actor_after_save

post_save.connect(actor_after_save, sender=Band)


def get_bandpicture_path(aBandPicture, filename):
    dst = 'bands/%d/pictures/%s' % (aBandPicture.band.id,
                                    filename)
    return dst

class BandPicture(ImageModel):
    """
    A picture of a band
    """
    class IKOptions:
        image_field = 'original_image'
        spec_module = 'band.imagespecs'

    original_image = models.ImageField(upload_to=get_bandpicture_path)
    band = ForeignKey(Band, related_name='pictures')

    def __unicode__(self):
        return "Picture for band %s" % self.band.name

class BandMember(models.Model):
    """
    A membership link between users and bands
    """
    class Meta:
        unique_together = ('user', 'band')

    user = ForeignKey(User, related_name='band_memberships')
    band = ForeignKey(Band, related_name='members')
    roles = ManyToManyField(BandRole)

    approved = BooleanField(default=False,
                            help_text=_('Whether the membership has been approved'))

    def __unicode__(self):
        return "%s of %s" % (self.user,
                             self.band)


    @models.permalink
    def get_absolute_url(self):
        return ('band:membership-manage', (self.band.slug,))
