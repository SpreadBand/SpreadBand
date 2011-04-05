from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site

from apps.band.models import Band

class BandIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    def get_queryset(self):
        return Band.objects.all()

site.register(Band, BandIndex)
