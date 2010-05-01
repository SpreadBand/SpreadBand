from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from authority.decorators import permission_required_or_403

from schedule.periods import Month

from bargain.models import Party, Contract

from .models import Venue
from .forms import VenueForm


@permission_required_or_403('venue_permission.add_venue')
def new(request):
    """
    register a new venue
    """
    return create_object(request,
                         form_class=VenueForm,
                         template_name='venue/venue_new.html',
                         )


def detail(request, venue_slug):
    """
    Show details about a venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    # Get the bargains we're involved into
    venue_type = ContentType.objects.get_for_model(venue)
    try:
        party = Party.objects.get(content_type__pk=venue_type.id,
                                  object_id=venue.id)
        contracts = Contract.objects.filter(parties__contractparty__party=party)
    except Party.DoesNotExist:
        contracts = []

    return object_detail(request,
                         queryset=Venue.objects.all(),
                         slug=venue_slug,
                         template_name='venue/venue_detail.html',
                         template_object_name='venue',
                         extra_context={'contracts': contracts},
                         )
                          
def list(request):
    """
    list all venues
    """
    return object_list(request,
                       queryset=Venue.objects.all(),
                       template_name='venue/venue_list.html',
                       template_object_name='venue',
                       )


