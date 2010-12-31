from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from django.conf import settings

from band.models import Band

from .models import Venue
from .forms import VenueForm, VenueUpdateForm, VenuePictureForm, NewCantFindForm

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

    # Cant Find form
    cantfind_form = NewCantFindForm()

    return render_to_response(template_name='venue/search.html',
                              dictionary={'venue_filter': venue_filter,
                                          'geosearch_form': geosearch_form,
                                          'ambiance_tags': ambiance_tags,
                                          'cantfind_form': cantfind_form},
                              context_instance=RequestContext(request)
                              )


from .forms import NewCantFindForm, SendNewCantFindForm

import math

from urllib2 import urlopen
import simplejson
from django.template.defaultfilters import removetags


GOOGLE_REVERSE_GEOCODE_URI = 'http://maps.google.com/maps/api/geocode/json?latlng=%(latitude)s,%(longitude)s&sensor=false&key=%(key)s'

def reverse_geocode(latitude, longitude):
    if not (-85 < latitude < 85) or not (-180 < longitude < 180):
        return ""

    url = GOOGLE_REVERSE_GEOCODE_URI % { 'key': settings.GOOGLE_MAPS_API_KEY, 'latitude': latitude, 'longitude': longitude }
    fp = urlopen(url)
    data = simplejson.load(fp)
    fp.close()

    status = data['status']
    if status != 'OK':
        return None
    else:
        return data['results'][0]['formatted_address']

def search_cantfind(request):   
    newcantfind_form = NewCantFindForm(request.GET)

    sendnewcantfind_form = SendNewCantFindForm(request.POST or request.GET)
    if sendnewcantfind_form.is_valid():
        x = sendnewcantfind_form.cleaned_data['x']
        y = sendnewcantfind_form.cleaned_data['y']
        distance = sendnewcantfind_form.cleaned_data['distance']
        ambiance = sendnewcantfind_form.cleaned_data['ambiance']

        if request.POST.get('submit', None):
            address = reverse_geocode(y, x)

            text = render_to_string(template_name='venue/search_cantfind_text.html',
                                    dictionary={'address': address,
                                                'distance': round(distance / 1000.0, 1),
                                                'sendnewcantfind_form': sendnewcantfind_form,
                                                'ambiance': ambiance,
                                                'user': request.user})
            
            send_mail("Une nouvelle mission pour SuperLaurent",
                      removetags(text, "input strong textarea label p"),
                      'noreply@spreadband.com',
                      [settings.VENUE_CANTFIND_EMAIL],
                      fail_silently=False)
            
            messages.success(request, _("A new mission was successfully sent to SuperLaurent !"))
            
            return redirect('venue:search')
        


    if newcantfind_form.is_valid():
        x = newcantfind_form.cleaned_data['x']
        y = newcantfind_form.cleaned_data['y']
        distance = newcantfind_form.cleaned_data['distance']
        ambiance = newcantfind_form.cleaned_data['ambiance']

        address = reverse_geocode(y, x)

        text = render_to_string(template_name='venue/search_cantfind_text.html',
                                dictionary={'address': address,
                                            'sendnewcantfind_form': sendnewcantfind_form,
                                            'distance': round(distance / 1000.0, 1),
                                            'ambiance': ambiance,
                                            'user': request.user})
    else:
        text = _("Type your text here !")
        
    return render_to_response(template_name='venue/search_cantfind.html',
                              dictionary={'text': text,
                                          'sendnewcantfind_form': sendnewcantfind_form},
                              context_instance=RequestContext(request)
                              )
