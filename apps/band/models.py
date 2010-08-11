from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, ManyToManyField, DateField, TextField, ForeignKey, BooleanField
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from tagging.fields import TagField
from imagekit.models import ImageModel
from elsewhere.models import SocialNetworkProfile, WebsiteProfile

from django_countries import CountryField
from actors.models import Actor
from minisite.models.minisite import Minisite
from world.models import Place


class Band(Actor):
    """
    A music band
    """
    class Meta:
        permissions = (
            ('can_manage', 'Can manage this band'),
        )

    name = CharField(max_length=200)
    
    slug = models.SlugField(max_length=40, unique=True)

    founded_on = DateField(help_text=_('When the band was founded'),
                           blank=True,
                           null=True)
    
    genres = TagField('Genres')

    city = CharField(max_length=100)
    zipcode = CharField(max_length=50)
    country = CountryField()
    # pointer to geo informations
    place = ForeignKey(Place, null=True, blank=True)


    biography = TextField(blank=True,
                          help_text=_('Band biography'))


    website = ForeignKey(Minisite, blank=True, null=True)

    members = ManyToManyField(User, through='BandMember', related_name='bands')

    technical_sheet = TextField(blank=True, null=True)

    socialnetworks = generic.GenericRelation(SocialNetworkProfile,
                                             object_id_field="object_id",
                                             content_type_field="content_type")


    websites = generic.GenericRelation(WebsiteProfile,
                                       object_id_field="object_id",
                                       content_type_field="content_type")

    #-- Functions
    def avatar_url(self):
        from django.conf import settings
        """
        Return the url of the avatar, or default to a 'no picture'
        picture
        """
        try:
            avatar = self.pictures.avatar()
            return avatar.avatar_image.url
        except:
            return settings.MEDIA_URL + '/images/tmp_band.jpg'
            

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


class BandPictureManager(models.Manager):
    def avatar(self):
        """
        Return the avatar of the band
        """
        return self.get(is_avatar=True)

class BandPicture(ImageModel):
    """
    A picture of a band
    """
    objects = BandPictureManager()

    class IKOptions:
        image_field = 'original_image'
        spec_module = 'band.imagespecs'

    class Meta:
        unique_together = ('band', 'is_avatar')

    original_image = models.ImageField(upload_to=get_bandpicture_path)
    band = ForeignKey(Band, related_name='pictures')

    title = CharField(max_length=100,
                      null=True, blank=True)

    description = CharField(max_length=255,
                            null=True, blank=True)

    is_avatar = BooleanField(default=False)

    def __unicode__(self):
        return "Picture for band %s" % self.band.name


class BandRole(models.Model):
    """
    A typed role in a band. Eg: guitarist
    """
    label = CharField(max_length=30,
                      unique=True)

    def __unicode__(self):
        return self.label

class BandMember(models.Model):
    """
    A membership link between users and bands
    """
    class Meta:
        unique_together = ('user', 'band')

    user = ForeignKey(User, related_name='band_memberships')
    band = ForeignKey(Band, related_name='band_members')
    roles = ManyToManyField(BandRole, related_name='roles')

    approved = BooleanField(default=False,
                            help_text=_('Whether the membership has been approved'))

    def __unicode__(self):
        return "%s of %s" % (self.user,
                             self.band)


    @models.permalink
    def get_absolute_url(self):
        return ('band:membership-manage', (self.band.slug,))
