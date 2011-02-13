import django_filters

from .models import Band

class BandFilter(django_filters.FilterSet):
    class Meta:
        model = Band
        fields = ('name',)

    name = django_filters.CharFilter()#lookup_type='contains')
