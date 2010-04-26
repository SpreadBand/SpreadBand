from django.db import models
from django.db.models import ForeignKey, CharField
from django.db.models.signals import post_save

from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = ForeignKey(User, unique=True)

    favorite_band = CharField(max_length=100, blank=True)


# Create a profile as soon as we create a user
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

post_save.connect(create_profile, sender=User)
