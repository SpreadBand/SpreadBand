from django.utils.translation import ugettext
_ = lambda u: unicode(ugettext(u))

from django.db import models
from django.db.models import CharField, SlugField, TextField, BooleanField, URLField
from django.db.models import ForeignKey, PositiveSmallIntegerField, ManyToManyField
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from django_countries import CountryField
from imagekit.models import ImageModel
from elsewhere.models import SocialNetworkProfile, WebsiteProfile
from tagging.fields import TagField

from actors.models import Actor
from world.models import Place

class Venue(Actor):
    """
    A place where a gig can happen
    """
    class Meta:
        permissions = (
            ('can_manage', _('Can manage this venue')),
        )

    name = CharField(verbose_name=_('name'),
                     max_length=200)
    slug = SlugField(max_length=100, unique=True)

    ambiance = TagField(verbose_name=_("ambiance"),
                        help_text=("Describe the style of music or atmosphere that represents your venue."))

    # address
    address = TextField(verbose_name=_('address'),
                        help_text=_("Street name and number. Don't enter your postal code, city and country (see below)."))
    city = CharField(verbose_name=_('city'),
                     max_length=100)
    zipcode = CharField(verbose_name=_('zipcode'),
                        max_length=50)
    country = CountryField(verbose_name=_('country'))
    # pointer to geo informations
    place = ForeignKey(Place, null=True, blank=True)
        

    description = TextField(verbose_name=_('description'),
                            help_text=_("Describe the ambiance of your venue: what kind of music do you usually play, what kind of people come, ..."))

    capacity = PositiveSmallIntegerField(verbose_name=_('capacity'),
                                         default=0,
                                         help_text=_('How many people can you welcome during a gig ?'))

    members = ManyToManyField(User, through='VenueMember', related_name='venues')

    socialnetworks = generic.GenericRelation(SocialNetworkProfile,
                                             object_id_field="object_id",
                                             content_type_field="content_type")

    websites = generic.GenericRelation(WebsiteProfile,
                                       object_id_field="object_id",
                                       content_type_field="content_type")

    video = URLField(verbose_name=_("video"),
                     help_text=_("Paste an URL from Youtube, Dailymotion, Vimeo or another video provider."),
                     max_length=500,
                     null=True,
                     blank=True)

    #-- Functions
    def avatar_url(self):
        from django.conf import settings
        """
        Return the url of the avatar, or default to a generic one
        """
        try:
            avatar = self.pictures.avatar()
            return avatar.avatar_image.url
        except:
            return settings.MEDIA_URL + '/images/venue/no_picture.png'


    def __unicode__(self):
        return u"%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('venue:detail', (self.slug,))


def get_venuepicture_path(aVenuePicture, filename):
    dst = 'venue/%d/pictures/%s' % (aVenuePicture.venue.id,
                                    filename)
    return dst


class VenuePictureManager(models.Manager):
    def avatar(self):
        """
        Return the avatar of the venue
        """
        return self.get(is_avatar=True)

class VenuePicture(ImageModel):
    """
    A picture of a venue
    """
    objects = VenuePictureManager()

    class IKOptions:
        image_field = 'original_image'
        spec_module = 'venue.imagespecs'

    original_image = models.ImageField(verbose_name=_('image'),
                                       upload_to=get_venuepicture_path)
    venue = ForeignKey(Venue, related_name='pictures')

    title = CharField(verbose_name=_('title'),
                      max_length=100,
                      null=True, blank=True)

    description = CharField(verbose_name=_('description'),
                            max_length=255,
                            null=True, blank=True)

    is_avatar = BooleanField(verbose_name=_("use as avatar ?"),
                             default=False,
                             help_text=_("Check this if you want to use this picture as your avatar"))

    def __unicode__(self):
        return _(u"Picture for venue %s") % self.venue.name


class VenueRole(models.Model):
    """
    A typed role in a venue. Eg: boss
    """
    class Meta:
        ordering = ('label',)

    label = CharField(max_length=30,
                      unique=True)

    def __unicode__(self):
        return self.label

class VenueMember(models.Model):
    """
    A membership link between users and venues
    """
    class Meta:
        unique_together = ('user', 'venue')

    user = ForeignKey(User, 
                      verbose_name=_('user'),
                      related_name='venue_memberships')

    venue = ForeignKey(Venue, related_name='venue_members')

    roles = ManyToManyField(VenueRole, 
                            verbose_name=_('Roles'),
                            related_name='roles')

    approved = BooleanField(default=False,
                            help_text=_('Whether the membership has been approved'))

    def __unicode__(self):
        return u"%s of %s" % (self.user,
                              unicode(self.venue))


    @models.permalink
    def get_absolute_url(self):
        return ('venue:membership-manage', (self.venue.slug,))




# This should be in actors.models, but django currently doesn't deal
# well with signals and inheritance
from django.db.models.signals import post_save
from actors.models import actor_after_save

post_save.connect(actor_after_save, sender=Venue)

# Reversions
import reversion
reversion.register(Venue)
