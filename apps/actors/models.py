from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import DateTimeField, BooleanField, OneToOneField

from agenda.models import Calendar
from annoying.fields import AutoOneToOneField

class Actor(models.Model):
    """
    An actor is an entity playing a role in your system. It can be anything that
    belongs to a user and interact during its workflow.
    """
    class meta:
        abstract = True

    registered_on = DateTimeField(auto_now_add=True,
                                  help_text=_('When it was was registered'),
                                  editable=False
                                  )
    
    last_activity = DateTimeField(auto_now=True,
                                  help_text=_('The last time something happened'),
                                  editable=False
                                  )

    owned = BooleanField(default=False,
                         help_text=_('Wether this actor is owned by at least one user')
                         )

    calendar = AutoOneToOneField(Calendar, null=True, blank=True, editable=False)

# def actor_after_save(sender, instance, created, **kwargs):
#     """
#     Called to ensure the calendar is created for a given actor
#     """
#     if created:
#         cal = Calendar(name='%s' % instance.name)
#         cal.save()
#         instance.calendar = cal
#         instance.save()










    
