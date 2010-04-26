from django.db.models import Model

class ModelStatsMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_class = type.__new__(cls, name, bases, attrs)
        return new_class


class ModelStats(object):
    __metaclass__  = ModelStatsMetaclass

from django.db.models import IntegerField, ForeignKey, CharField, PositiveIntegerField

class StatsIndex(ForeignKey):
    def __init__(self, field_name):
        # Compute new attributes
        attributes = {'__module__': __name__,
                      'key': CharField(max_length=255),
                      'value': PositiveIntegerField(default=0)}

        self.dbclass = type.__new__(type,
                                    "Stats%s" % (field_name),
                                    (Model,),
                                    attributes,
                                    )

        ForeignKey.__init__(self, self.dbclass)


class InstanceCount(IntegerField):
    def __init__(self):
        IntegerField.__init__(self, default=0)
