import django_filters

from .models import Band
from tagging.utils import parse_tag_input

def filter_tags(queryset, value):
    if value:
        # Filter bands that matches
        for tag in parse_tag_input(value):
            queryset = queryset.filter(genres__contains=tag)

    return queryset

class BandFilter(django_filters.FilterSet):
    class Meta:
        model = Band
        fields = ('name', 'genres')

    name = django_filters.CharFilter(lookup_type='contains')
    genres = django_filters.CharFilter(action=filter_tags)
