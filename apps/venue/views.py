from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from band.models import Band

from .models import Venue
from .forms import VenueForm, VenueUpdateForm, VenuePictureForm

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
    Show public page of a Venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    # Five latest gigs
    latest_bands = Band.objects.filter(id__in=venue.gigs.past_events()[:5]).distinct()

    past_events = venue.gigs.past_events()[:1]
    future_events = venue.gigs.future_events()[0:5]

    extra_context = {'latest_bands': latest_bands,
                     'past_events': past_events,
                     'future_events': future_events}

    # Get the bargains we're involved into
    return object_detail(request,
                         queryset=Venue.objects.all(),
                         slug=venue_slug,
                         template_name='venue/venue_detail.html',
                         template_object_name='venue',
                         extra_context=extra_context,
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


from geopy import geocoders
from django.conf import settings
from django.contrib.gis.geos import Point
from world.models import Place

@login_required
def edit(request, venue_slug):
    """
    Edit a venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    if request.method == 'POST':
        venue_form = VenueUpdateForm(request.POST, request.FILES,
                                     instance=venue)

        if venue_form.is_valid():
            venue = venue_form.save(commit=False)
            g = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)
            geoplace, (lat, lng) = g.geocode('%s, %s, %s, %s' % (venue.address,
                                                                 venue.zipcode,
                                                                 venue.city,
                                                                 venue.country),
                                             exactly_one=True,
                                             )

            # Edit
            point = Point(lng, lat)
            if venue.place:
                place = venue.place
                place.address = geoplace
                place.geom = point
                place.save()
            else:
                place = Place.objects.create(address=geoplace, geom=point)

            venue.place = place
            venue.save()

            return redirect(venue)

    return update_object(request,
                         form_class=VenueUpdateForm,
                         slug=venue_slug,
                         template_name='venue/venue_update.html',
                         extra_context={'venue': venue},
                         )


#--- PICTURES
def picture_new(request, venue_slug):
    venue = get_object_or_404(Venue, slug=venue_slug)

    if request.method == 'POST':
        picture_form = VenuePictureForm(request.POST, request.FILES)

        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.venue = venue

            picture.save()

            return redirect(venue)

    return create_object(request,
                         form_class=VenuePictureForm,
                         template_name='venue/picture_new.html',
                         extra_context={'venue': venue}
                         )
