import django_filters

from .models import Venue
from tagging.utils import parse_tag_input

class VenueFilter(django_filters.FilterSet):
    class Meta:
        model = Venue
        fields = ('name', 'ambiance')

    name = django_filters.CharFilter(lookup_type='contains')

