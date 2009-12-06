from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, ManyToManyField, DateField, DateTimeField, TextField
from django.contrib.auth.models import User

from schedule.models import Calendar
from tagging.fields import TagField
from photologue.models import Gallery

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

    founded_on = DateField(help_text=_('When the band was founded'))
    
    registered_on = DateTimeField(auto_now_add=True,
                                  help_text=_('When the band was registered')
                                  )
    
    last_activity = DateTimeField(auto_now_add=True,
                                  help_text=_('The last time something happened')
                                  )
    
    style_tags = TagField('Styles')

    biography = TextField(help_text=_('Band biography'))
    
    members = ManyToManyField(BandMember,
                              blank=True,
                              help_text=_('Active members')
                              )

    calendar = models.ForeignKey(Calendar,
                                 help_text=_('Event calendar')
                                 )
    
    photos = models.ForeignKey(Gallery,
                               help_text=_('Photo gallery')
                               )
    
    def __unicode__(self):
        return self.name



