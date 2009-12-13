from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import DateTimeField

from schedule.models import Calendar

class Actor(models.Model):
    """
    An actor is an entity playing a role in your system. It can be anything that
    belongs to a user and interact during its workflow.
    """
    class meta:
        abstract = True

    registered_on = DateTimeField(auto_now_add=True,
                                  help_text=_('When it was was registered')
                                  )
    
    last_activity = DateTimeField(auto_now_add=True,
                                  help_text=_('The last time something happened')
                                  )

    #-- Properties
    def _get_calendar(self):
        return Calendar.objects.get_or_create_calendar_for_object(self)
    
    calendar = property(_get_calendar)




    
