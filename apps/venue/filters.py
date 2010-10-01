import django_filters

from .models import Venue
from tagging.utils import parse_tag_input

def filter_tags(queryset, value):
    if value:
        # we assume if no ambiance is specified, then we are
        # compatible with everything
        without_ambiance_qs = queryset.filter(ambiance='')

        # Filter people that matches
        for tag in parse_tag_input(value):
            queryset = queryset.filter(ambiance__contains=tag)

        queryset = queryset | without_ambiance_qs

    return queryset

class VenueFilter(django_filters.FilterSet):
    class Meta:
        model = Venue
        fields = ('name', 'ambiance')

    ambiance = django_filters.CharFilter(action=filter_tags)
