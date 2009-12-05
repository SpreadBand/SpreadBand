from django.db.models import CharField

from tagging.fields import TagField

from actors.models import Actor

class Band(Actor):
    name = CharField(max_length=200)
    style_tags = TagField()

    def __str__(self):
        return self.name



