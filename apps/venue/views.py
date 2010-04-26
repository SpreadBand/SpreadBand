from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail

from authority.decorators import permission_required_or_403

from schedule.periods import Month

from .models import Venue
from .forms import VenueForm


@permission_required_or_403('venue_permission.add_gigplace')
def new(request):
    """
    register a new venue
    """
    return create_object(request,
                         form_class=VenueForm,
                         template_name='venue/venue_new.html',
                         )


def detail(request, venue_id):
    """
    Show details about a venue
    """
    period = [Month]
    return object_detail(request,
                         queryset=Venue.objects.all(),
                         object_id=venue_id,
                         template_name='venue/venue_detail.html',
                         template_object_name='venue',
                         extra_context={"period" : period},
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


