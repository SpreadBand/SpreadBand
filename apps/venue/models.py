from django.utils.translation import ugettext
_ = lambda u: unicode(ugettext(u))

from django.db import models
from django.db.models import CharField, SlugField, TextField, BooleanField, URLField
from django.db.models import ForeignKey, PositiveSmallIntegerField
from django.contrib.contenttypes import generic

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

    name = CharField(max_length=200)
    slug = SlugField(max_length=100, unique=True)

    ambiance = TagField()

    # address
    address = TextField()
    city = CharField(max_length=100)
    zipcode = CharField(max_length=50)
    country = CountryField()
    # pointer to geo informations
    place = ForeignKey(Place, null=True, blank=True)
        

    description = TextField()

    capacity = PositiveSmallIntegerField(default=0,
                                         help_text=_('Capacity of the room'))

    socialnetworks = generic.GenericRelation(SocialNetworkProfile,
                                             object_id_field="object_id",
                                             content_type_field="content_type")

    websites = generic.GenericRelation(WebsiteProfile,
                                       object_id_field="object_id",
                                       content_type_field="content_type")

    video = URLField(max_length=500,
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
            return settings.MEDIA_URL + '/images/tmp_venue.jpg'


    def __unicode__(self):
        return self.name

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

    original_image = models.ImageField(upload_to=get_venuepicture_path)
    venue = ForeignKey(Venue, related_name='pictures')

    title = CharField(max_length=100,
                      null=True, blank=True)

    description = CharField(max_length=255,
                            null=True, blank=True)

    is_avatar = BooleanField(default=False)

    def __unicode__(self):
        return _("Picture for venue %s") % self.venue.name




# This should be in actors.models, but django currently doesn't deal
# well with signals and inheritance
from django.db.models.signals import post_save
from actors.models import actor_after_save

post_save.connect(actor_after_save, sender=Venue)
