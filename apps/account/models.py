import datetime

from django.db import models
from django.db.models import ForeignKey, CharField, DateField, OneToOneField
from django.db.models.signals import post_save

from django.contrib.auth.models import User

from imagekit.models import ImageModel

from django_countries import CountryField
from timezones.fields import TimeZoneField

class UserProfile(models.Model):
    """
    A profile for a user
    """
    genre_choices = (('M', 'Male'),
                     ('F', 'Female'))

    user = ForeignKey(User, unique=True)
    birthdate = DateField(null=True, blank=True)

    genre = CharField(max_length=1, blank=True,
                      choices=genre_choices)

    country = CountryField()
    timezone = TimeZoneField()

    town = CharField(max_length=50, blank=True)

    @property
    def age(self):
        """
        Calculate the age of a user
        """
        if self.birthdate:
            d = datetime.date.today()
            return (d.year - self.birthdate.year) - int((d.month, d.day) < (self.birthdate.month, self.birthdate.day))
        else:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ("account:detail", (self.user,), {})

    def __unicode__(self):
        return "Profile for %s" % self.user


def get_useravatar_path(aUserAvatar, filename):
    dst = 'users/%d/avatar/%s' % (aUserAvatar.userprofile.id,
                                  filename)
    return dst

class UserAvatar(ImageModel):
    """
    An avatar of a user
    """
    class IKOptions:
        image_field = 'original_image'
        spec_module = 'account.imagespecs'

    original_image = models.ImageField(upload_to=get_useravatar_path)

    userprofile = OneToOneField(UserProfile,
                                related_name='avatar')


    def __unicode__(self):
        return "Avatar for %s" % self.userprofile.user


# Create a profile as soon as we create a user
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

post_save.connect(create_profile, sender=User)
