from actors.models import Actor
from django.db.models import CharField

class Band(Actor):
    name = CharField(max_length=200)



