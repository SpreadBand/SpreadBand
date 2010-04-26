from django.db.models import Model, DateField, ForeignKey, PositiveIntegerField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class OrmBackendDaily(Model):
    date = DateField()
    
    content_type = ForeignKey(ContentType, related_name="watched_object")
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


from django.db.models import Field

def get_fields(aModelStats):
    for name, field in aModelStats.__dict__.iteritems():
        if isinstance(field, Field):
            yield name, field
            

from .models import InstanceCount

class OrmBackend(object):
    def __init__(self, aModelStats):
        self.modelstats = aModelStats

        simple_fields = {}
        indexed_fields = []

        for name, field in get_fields(aModelStats):
            if isinstance(field, Field):
                simple_fields[name] = field

        # Compute new attributes
        attributes = {'__module__': __name__,
                      'date': DateField(auto_now_add=True)}

        attributes.update(simple_fields)

        self.dbstats_class = type.__new__(type,
                                          aModelStats.__name__,
                                          (Model,),
                                          attributes,
                                          )


    def on_save(self, instance, created, **kwargs):
        """
        Generic dispatch when a model is saved
        """
        from datetime import datetime
        today = datetime.today()
        dbstats = self.dbstats_class.objects.get_or_create(date=today)[0]

        if created:
            self.new(instance, dbstats)
        else:
            self.update(instance, dbstats)

        dbstats.save()
    
    def new(self, aModel, aDBStats):
        """
        Called when a new model is created
        """
        print "newwww model", aModel

        # Update the InstanceCount field if we count instances
        for name, field in aDBStats.__dict__.iteritems():
            if isinstance(field, InstanceCount):
                aDBStats.setattr(name,
                                 aDBStats.getattr(name) + 1)
                                 
            

    def update(self, aModel, aDBStats):
        """
        Called when a model is updated
        """
        print
        print "update modellll", aModel, aDBStats
        print

        aDBStats.count = 1



