import uuid
import os

from django.utils.translation import ugettext
_ = lambda u: unicode(ugettext(u))

from django.db import models
from django.db.models import CharField, ManyToManyField, DateField, TextField, ForeignKey, BooleanField
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from tagging.fields import TagField
from imagekit.models import ImageModel
from elsewhere.models import SocialNetworkProfile, WebsiteProfile
from badges.models import BadgeToLaureate
from django_countries import CountryField

from apps.actors.models import Actor
from world.models import Place
# from minisite.models.minisite import Minisite


class Band(Actor):
    """
    A music band
    """
    class Meta:
        permissions = (
            ('can_manage', _('Can manage this band')),
        )

        ordering = ('name',)

    name = CharField(verbose_name=_('Name'),
                     max_length=200)
    
    slug = models.SlugField(verbose_name=_('Slug'),
                            max_length=40, unique=True)

    founded_on = DateField(verbose_name=_('Founded on'),
                           help_text=_('When the band was founded'),
                           blank=True,
                           null=True)
    
    genres = TagField(verbose_name=_('genres'),
                      help_text=_("Describe your music using tags such as: rock metal progressive.")
                      )

    influences = CharField(verbose_name=_('influences'),
                           help_text=_("The other artists that make your band what it is."),
                           max_length=200,
                           blank=True,
                           null=True)

    city = CharField(verbose_name=_('city'),
                     help_text=_("Where is your band from ?"),
                     max_length=100)

    zipcode = CharField(verbose_name=_('Zipcode'),
                        max_length=50)

    country = CountryField(verbose_name=_('Country'))
    # pointer to geo informations
    place = ForeignKey(Place, null=True, blank=True)


    biography = TextField(verbose_name=_('Biography'),
                          blank=True,
                          help_text=_('Who are the people inside your band ? How was it created ? Why are you doing this ?...')
                          )


    # website = ForeignKey(Minisite, blank=True, null=True)

    members = ManyToManyField(User, through='BandMember', related_name='bands')

    technical_sheet = TextField(verbose_name=_('Technical Sheet'),
                                help_text=_("What kind of gear do you need on stage ? What do you bring ? What do you expect from the venue ?"),
                                blank=True, null=True
                                )

    socialnetworks = generic.GenericRelation(SocialNetworkProfile,
                                             object_id_field="object_id",
                                             content_type_field="content_type"
                                             )


    websites = generic.GenericRelation(WebsiteProfile,
                                       object_id_field="object_id",
                                       content_type_field="content_type")

    badges = generic.GenericRelation(BadgeToLaureate,
                                     object_id_field='laureate_object_id',
                                     content_type_field='laureate_content_type')


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
            return settings.MEDIA_URL + '/images/band/no_picture.png'
            

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
    """
    Generate a random UUID for a picture,
    use the uuid as the picture name
    """
    picture_uuid = uuid.uuid4()
    name, extension = os.path.splitext(filename)

    dst = 'bands/%d/pictures/%s%s' % (aBandPicture.band.id,
                                      picture_uuid,
                                      extension)

    return dst


class BandPictureManager(models.Manager):
    def avatar(self):
        """
        Return the avatar of the band
        """
        avatar = self.filter(is_avatar=True)
        if avatar:
            return avatar[0]
        else:
            return None

class BandPicture(ImageModel):
    """
    A picture of a band
    """
    objects = BandPictureManager()

    class IKOptions:
        image_field = 'original_image'
        spec_module = 'band.imagespecs'

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
    class Meta:
        ordering = ('label',)

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

    user = ForeignKey(User, 
                      verbose_name=_('user'),
                      related_name='band_memberships')

    band = ForeignKey(Band, related_name='band_members')

    roles = ManyToManyField(BandRole, 
                            verbose_name=_('Roles'),
                            related_name='roles')

    approved = BooleanField(default=False,
                            help_text=_('Whether the membership has been approved'))

    def __unicode__(self):
        return "%s of %s" % (self.user,
                             self.band)


    @models.permalink
    def get_absolute_url(self):
        return ('band:membership-manage', (self.band.slug,))


#--- Signals ---#
from annoying.decorators import signals
from oauth_access.models import OAuthAssociation
from elsewhere.models import SocialNetwork, SocialNetworkProfile
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

@signals.post_save(sender=OAuthAssociation)
def add_band_socialnetwork_on_auth_assoc(sender, instance, created, **kwargs):
    if created:
        band_ctype = ContentType.objects.get_for_model(Band)

        # Check if we're saving a social net for a band
        if instance.content_type == band_ctype:
            band = instance.associated_object

            # Lookup which social network we've subscribed to
            try:
                net = SocialNetwork.objects.get(name__iexact=instance.service)
            except SocialNetwork.DoesNotExist:
                # If we don't know it, don't create anything
                return

            # Check if we already have this network created
            try:
                SocialNetworkProfile.objects.get(content_type=band_ctype,
                                                 object_id=band.id)
            except SocialNetworkProfile.DoesNotExist:
                # if not, create it
                SocialNetworkProfile.objects.create(content_type=band_ctype,
                                                    object_id=band.id,
                                                    network=net,
                                                    username=instance.identifier)


import meta_badges
