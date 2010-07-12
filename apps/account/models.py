from django.db import models
from django.db.models import ForeignKey, CharField, DateField
from django.db.models.signals import post_save

from django.contrib.auth.models import User

from django_countries import CountryField
from timezones.fields import TimeZoneField

# Create your models here.
class UserProfile(models.Model):
    user = ForeignKey(User, unique=True)

    country = CountryField()
    timezone = TimeZoneField()

    town = CharField(max_length=50, blank=True)
    birthdate = DateField(null=True, blank=True)


# Create a profile as soon as we create a user
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

post_save.connect(create_profile, sender=User)
