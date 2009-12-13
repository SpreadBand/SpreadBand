from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, ManyToManyField, DateField, DateTimeField, TextField, ForeignKey
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
    user = ForeignKey(User)
    role = ForeignKey(BandRole,
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
    
    style_tags = TagField('Styles')

    biography = TextField(blank=True,
                          help_text=_('Band biography'))
    
    members = ManyToManyField(BandMember,
                              blank=True,
                              help_text=_('Active members')
                              )
    
    photos = ForeignKey(Gallery,
                        null=True,
                        help_text=_('Photo gallery')
                        )

    def _get_visibility(self):
        """
        Return the visibility based on the subscription

        XXX: For now, it's hardcoded as 'one month visibility'
        """
        from datetime import datetime
        now = datetime.now()
        next_month = now.replace(month=now.month + 1)
        return next_month
    
    visibility = property(_get_visibility)

    #-- Properties
    def _get_calendar(self):
        return Calendar.objects.get_or_create_calendar_for_object(self)
    
    calendar = property(_get_calendar)

    #-- Functions
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('bands.views.detail', [str(self.id)])

