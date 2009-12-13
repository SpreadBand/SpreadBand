from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, ForeignKey

from photologue.models import Gallery

from actors.models import Actor

class GigPlace(Actor):
    """
    A place where a gig can happen
    """
    name = CharField(max_length=200)

    photos = ForeignKey(Gallery,
                        null=True,
                        help_text=_('Photo gallery')
                        )

    @models.permalink
    def get_absolute_url(self):
        return ('gigplaces.views.detail', [str(self.id)])
