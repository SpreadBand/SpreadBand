from django.db import models

from django.db.models import CharField, TextField
from django.db.models import ForeignKey

class Layout(models.Model):
    """
    A template layout for a minisite
    """
    class Meta:
        app_label = 'minisite'

    name = CharField(max_length=100)
    template = TextField()

    def __unicode__(self):
        return self.name


class Minisite(models.Model):
    """
    A minisite instance
    """
    class Meta:
        app_label = 'minisite'

    layout = ForeignKey(Layout)
