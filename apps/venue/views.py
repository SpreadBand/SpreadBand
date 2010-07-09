from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from bargain.models import Party, Contract

from .models import Venue
from .forms import VenueForm, VenueUpdateForm


@login_required
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
    return object_detail(request,
                         queryset=Venue.objects.all(),
                         slug=venue_slug,
                         template_name='venue/venue_detail.html',
                         template_object_name='venue',
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


@login_required
def edit(request, venue_slug):
    """
    Edit a venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    return update_object(request,
                         form_class=VenueUpdateForm,
                         slug=venue_slug,
                         template_name='venue/venue_update.html',
                         extra_context={'venue': venue},
                         )


