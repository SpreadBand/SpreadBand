from django.db import models
from django.db.models import CharField, ManyToManyField, DateTimeField, TextField
from django.contrib.auth.models import User

from schedule.models import Calendar
from tagging.fields import TagField

from actors.models import Actor


class BandRole(models.Model):
    """
    A typed role in a band. Eg: guitarist
    """
    label = CharField(max_length=30)

    def __unicode__(self):
        return self.label

class BandMember(models.Model):
    """
    A membership link between users and bands
    """
    user = models.ForeignKey(User)
    role = models.ForeignKey(BandRole,
                             unique=True)

    def __unicode__(self):
        return "%s (%s)" % (self.user,
                            self.role)

class Band(Actor):
    """
    A music band
    """
    name = CharField(max_length=200)
    
    created_on = DateTimeField('When the band was registered',
                               auto_now_add=True)
    
    last_activity = DateTimeField('The last time something happened',
                                  auto_now_add=True)
    
    style_tags = TagField('Styles')

    biography = TextField()
    
    members = ManyToManyField(BandMember,
                              blank=True)

    calendar = models.ForeignKey(Calendar)
                                 
    def __unicode__(self):
        return self.name



