from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import CharField, SlugField, TextField
from django.db.models import ForeignKey

from photologue.models import Gallery
from tagging.fields import TagField

from actors.models import Actor

class Venue(Actor):
    """
    A place where a gig can happen
    """
    name = CharField(max_length=200)
    slug = SlugField(max_length=100, unique=True)

    ambiance = TagField()

    description = TextField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('venue:detail', (self.slug,))
