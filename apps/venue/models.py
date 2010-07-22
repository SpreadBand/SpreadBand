from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, SlugField, TextField
from django.db.models import ForeignKey

from tagging.fields import TagField

from actors.models import Actor

class Venue(Actor):
    """
    A place where a gig can happen
    """
    class Meta:
        permissions = (
            ('manages', 'Manages this venue'),
        )

    name = CharField(max_length=200)
    slug = SlugField(max_length=100, unique=True)

    ambiance = TagField()

    description = TextField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('venue:detail', (self.slug,))

# This should be in actors.models, but django currently doesn't deal
# well with signals and inheritance
# from django.db.models.signals import post_save
# from actors.models import actor_after_save

# post_save.connect(actor_after_save, sender=Venue)
