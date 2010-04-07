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
    
    style_tags = TagField('Styles')

    biography = TextField(blank=True,
                          help_text=_('Band biography'))


    website = ForeignKey(Minisite, blank=True, null=True)
    
    #-- Functions
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('band:detail',  (self.slug,))

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
        spec_module = 'bands.imagespecs'

    original_image = models.ImageField(upload_to=get_bandpicture_path)
    band = ForeignKey(Band, related_name='pictures')

    def __unicode__(self):
        return "Picture for band %s" % self.band.name

class BandMember(models.Model):
    """
    A membership link between users and bands
    """
    user = ForeignKey(User, related_name='band_memberships')
    band = ForeignKey(Band, related_name='members')
    role = ForeignKey(BandRole)

    approved = BooleanField(default=False,
                            help_text=_('Whether the membership has been approved'))

    def __unicode__(self):
        return "%s (%s)" % (self.user,
                            self.role)
