from django.db import models

class Actor(models.Model):
    """
    An actor is an entity playing a role in your system. It can be anything that
    belongs to a user and interact during its workflow.
    """

    class meta:
        abstract = True

    
