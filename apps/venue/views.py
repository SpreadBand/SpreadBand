from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

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

    # make a calendar
    from datetime import date
    from event.views.calendar import GigMonthlyHTMLCalendar
    monthly_calendar = GigMonthlyHTMLCalendar(firstweekday=0,
                                              aQueryset=venue.gigs.all(),
                                              when=date.today())

    # Check if the venue is managed
    is_managed = request.user.has_perm('venue.can_manage', venue)

    extra_context = {'latest_bands': latest_bands,
                     'past_events': past_events,
                     'future_events': future_events,
                     'monthly_calendar': monthly_calendar,
                     'is_managed': is_managed}

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
            try:
                geoplace, (lat, lng) = g.geocode('%s, %s, %s, %s' % (venue.address,
                                                                     venue.zipcode,
                                                                     venue.city,
                                                                     venue.country),
                                                 exactly_one=True,
                                                 )
            except geocoders.google.GQueryError, e:
                geoplace = "(Unable to resolve address)"
                (lat, lng) = (50.63, 3.06)

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

from .filters import VenueFilter

from geopy import geocoders
from django.utils.translation import gettext as _
from django.contrib.gis.measure import D
from django.core.paginator import Paginator

from .forms import VenueGeoSearchForm

from django_countries import countries

def lookup_place(city, country):
    g = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)

    # Ugly hack to get a place from geocoders -_-
    where = '%s, %s' % (city,
                        country)

    geoplace = _("Unable to lookup address")
    lat = lng = 0
    for match in g.geocode(where.encode('utf-8'),
                           exactly_one=False):
        geoplace, (lat, lng) = match
        # Get the first result
        break

    return Point(lng, lat)

def search_venue_atomic(data, center, distance, ambiance):
    venue_filter = VenueFilter(data, queryset=Venue.objects.all())

    # # If we have a distance, do a geo lookup
    # if distance and city and country:
    #     try:
    #         point = lookup_place(city, countries.OFFICIAL_COUNTRIES[country])
    #     except geocoders.google.GQueryError, e:
    #         geosearch_form.errors['city'] = _('Unable to find this city. Check the country or be more specific.')
    #     else:
    #         places = Place.objects.filter(geom__distance_lte=(point, D(m=distance)))
    #         venue_filter.queryset = venue_filter.queryset.filter(place__in=places.all())
    # Otherwise, try to match by name
    
    places_in_range = Place.objects.filter(geom__distance_lte=(center, D(m=distance)))
    venue_filter.queryset = venue_filter.queryset.filter(place__in=places_in_range.all())
    # else:
    # if city:
    #     venue_filter.queryset = venue_filter.queryset.filter(city__iexact=city)
    # if country:
    #     venue_filter.queryset = venue_filter.queryset.filter(country__iexact=country)

    return venue_filter



@login_required
def search(request):
    # Reconstruct the ambiance list since we use a multivariable trick
    ambiance_tags = request.GET.getlist("ambiance") or []

    # if we haven't specified anything, use the user place as a starting point
    if not request.GET:
        center = Point(0, 0)
        try:
            country = countries.OFFICIAL_COUNTRIES[request.user.get_profile().country or 'FR']
            town = request.user.get_profile().town
            if country and town:
                center = lookup_place(town, country)
        except geocoders.google.GQueryError, e:
            pass
        
    geosearch_form = VenueGeoSearchForm(request.GET or {'circle_x': center.x,
                                                        'circle_y': center.y,
                                                        'distance': 3500})

    if geosearch_form.is_valid():
        city = geosearch_form.cleaned_data.get('city')
        country = geosearch_form.cleaned_data.get('country')
        distance = geosearch_form.cleaned_data.get('distance')
        circle_x = geosearch_form.cleaned_data.get('circle_x')
        circle_y = geosearch_form.cleaned_data.get('circle_y')

        
    # Run the filters
    center_point = Point(circle_x, circle_y)
    venue_filter = search_venue_atomic(request.GET, center_point, distance, ambiance_tags)

    return render_to_response(template_name='venue/search.html',
                              dictionary={'venue_filter': venue_filter,
                                          'geosearch_form': geosearch_form,
                                          'ambiance_tags': ambiance_tags},
                              context_instance=RequestContext(request)
                              )
