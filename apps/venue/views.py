from datetime import datetime, timedelta

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
from presskit.models import PresskitViewRequest
from visitors.utils import record_visit, get_latest_visits_for

from presskit.signals import presskitview_venue_comment, presskitview_accepted_by_venue, presskitview_refused_by_venue

from .models import Venue
from .forms import VenueForm, VenueUpdateForm, VenuePictureForm, NewCantFindForm, VenueCreateForm, VenueMemberRequestForm

## XXX Security
@login_required
def presskit_viewrequest_venue_comment(request, venue_slug, viewrequest_id):
    viewrequest = get_object_or_404(PresskitViewRequest, venue__slug=venue_slug, pk=viewrequest_id)
    presskitview_venue_comment.send(sender=viewrequest)
    return redirect('venue:presskit-viewrequest-venue', venue_slug, viewrequest_id)
    

## XXX Security
@login_required
def presskit_viewrequest_venue(request, venue_slug, viewrequest_id):
    viewrequest = get_object_or_404(PresskitViewRequest, venue__slug=venue_slug, pk=viewrequest_id)

    # If pending, set it as seen
    if viewrequest.state == 'P':
        viewrequest.state = 'S'
        viewrequest.save()
    
    return render_to_response(template_name='presskit/presskit_viewrequest_venue.html',
                              dictionary={'venue': viewrequest.venue,
                                          'band': viewrequest.presskit.band,
                                          'presskit': viewrequest.presskit,
                                          'viewrequest': viewrequest},
                              context_instance=RequestContext(request)
                              )

## XXX Security
@login_required
def presskit_viewrequest_venue_accept(request, venue_slug, viewrequest_id):
    viewrequest = get_object_or_404(PresskitViewRequest, venue__slug=venue_slug, pk=viewrequest_id)
    
    viewrequest.state = 'A'
    viewrequest.save()

    # Notify
    presskitview_accepted_by_venue.send(sender=viewrequest)

    messages.success(request,
                     _("You have accepted to set up a gig with %s" % viewrequest.presskit.band.name))


    return redirect('venue:presskit-viewrequest-venue', venue_slug=venue_slug, viewrequest_id=viewrequest_id)


## XXX Security
@login_required
def presskit_viewrequest_venue_refuse(request, venue_slug, viewrequest_id):
    viewrequest = get_object_or_404(PresskitViewRequest, venue__slug=venue_slug, pk=viewrequest_id)
    
    viewrequest.state = 'D'
    viewrequest.save()

    # Notify
    presskitview_refused_by_venue.send(sender=viewrequest)

    messages.info(request,
                  _("You have refused to set up a gig with %s" % viewrequest.presskit.band.name))

    return redirect('venue:presskit-viewrequest-venue', venue_slug=venue_slug, viewrequest_id=viewrequest_id)




@login_required
def dashboard(request, venue_slug):
    """
    Dashboard for a venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    # Check perms
    if not request.user.has_perm('venue.can_manage', venue):
        return HttpResponseForbidden('You are not allowed to manage this venue')

    # Presskit tracker
    # Show either 30 latest days or the latest 15 presskits
    ten_days_ago = datetime.now() - timedelta(days=30)
    received_presskits = PresskitViewRequest.objects.filter(venue=venue,
                                                            modified_on__gte=ten_days_ago).order_by('modified_on', '-sent_on', 'state')[:15]


    # Get latest visits
    latest_visits = get_latest_visits_for(venue)

    return render_to_response(template_name='venue/dashboard.html',
                              dictionary={'venue': venue,
                                          'received_presskits': received_presskits,
                                          'latest_visits': latest_visits},
                              context_instance=RequestContext(request)
                              )
    

@login_required
def new(request):
    """
    register a new venue
    """
    create_form = VenueCreateForm(request.POST or None)
    member_form = VenueMemberRequestForm(request.POST or None)

    if request.method == 'POST':
        if member_form.is_valid():
            if create_form.is_valid():
                # Create the venue
                venue = create_form.save()
                
                # Add this user into the venue
                venuemember = VenueMember(venue=venue,
                                          user=request.user
                                          )
                venuemember.save()
                venuemember.roles = member_form.cleaned_data.get('roles')
                venuemember.save()
                
                # Assign rights to the user
                assign('venue.can_manage', venuemember.user, venue)
               
                return redirect(venue)

    return render_to_response(template_name='venue/venue_new.html',
                              dictionary={'form': create_form,
                                          'member_form': member_form},
                              context_instance=RequestContext(request)
                              )

def detail(request, venue_slug):
    """
    A view to route to the dashboard or the public depending on the
    rights of the user
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    # Check if the venue is managed
    is_managed = request.user.has_perm('venue.can_manage', venue)

    if is_managed:
        return redirect('venue:dashboard', venue.slug)
    else:
        return redirect('venue:profile', venue.slug)

def my_public_view(request, venue_slug):
    """
    Public profile when seen by the owner
    """
    return public_view(request, venue_slug, template_name='venue/myprofile.html')

def public_view(request, venue_slug, template_name='venue/venue_detail.html'):
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

    # if this is not our venue, then record us as a visitor
    # Venues
    if not is_managed:
        for venue in request.user.venues.all():
            record_visit(venue, venue)
            
        for band in request.user.bands.all():
            record_visit(band, venue)


    extra_context = {'latest_bands': latest_bands,
                     'past_events': past_events,
                     'future_events': future_events,
                     'monthly_calendar': monthly_calendar,
                     'is_managed': is_managed}

    # Get the bargains we're involved into
    return object_detail(request,
                         queryset=Venue.objects.all(),
                         slug=venue_slug,
                         template_name=template_name,
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

# XX: Security
@login_required
def picture_list(request, venue_slug):
    venue = get_object_or_404(Venue, slug=venue_slug)

    return object_list(request,
                       queryset=venue.pictures.all(),
                       template_name='venue/picture_list.html',
                       template_object_name='picture',
                       extra_context={'venue': venue},
                       )


# XX: Security
@login_required
def picture_new(request, venue_slug):
    venue = get_object_or_404(Venue, slug=venue_slug)

    if request.method == 'POST':
        picture_form = VenuePictureForm(request.POST, request.FILES)

        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.venue = venue

            picture.save()

            return redirect('venue:venue-pictures', venue.slug)

    return create_object(request,
                         form_class=VenuePictureForm,
                         template_name='venue/picture_new.html',
                         extra_context={'venue': venue}
                         )


# XXX: Security
@login_required
def picture_delete(request, venue_slug, picture_id):
    venue = get_object_or_404(Venue, slug=venue_slug)
    picture = get_object_or_404(venue.pictures, id=picture_id)

    picture.delete()

    return redirect('venue:venue-pictures', venue.slug)

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
            
            send_mail(_("Une nouvelle mission pour SuperLaurent"),
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



"""
Membership management for a venue

This code is fucking duplicated from the band management
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic.create_update import delete_object, create_object
from django.views.generic.list_detail import object_list

from guardian.shortcuts import assign, remove_perm

from .forms import VenueMemberAddForm
from .models import Venue, VenueMember

@login_required
def membership_add(request, venue_slug):
    """
    Add a member in the venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    # Permissions
    if not request.user.has_perm('venue.can_manage', venue):
        return HttpResponseForbidden(_("You are not allowed to edit this venue"))

    if request.method == 'POST':
        addform = VenueMemberAddForm(request.POST)

        if addform.is_valid():
            # Set venue
            venuemember = addform.save(commit=False)
            
            venuemember.venue = venue

            # Save to DB
            venuemember.save()
            addform.save_m2m()

            # Assign rights to the user
            assign('venue.can_manage', venuemember.user, venue)
            

            return redirect(venuemember)

    return create_object(request,
                         form_class=VenueMemberAddForm,
                         template_name='venue/membership_add.html',
                         extra_context={'venue': venue},
                         )

@login_required
def membership_manage(request, venue_slug):
    """
    Manage members in the venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    # Permissions
    if not request.user.has_perm('venue.can_manage', venue):
        return HttpResponseForbidden('You are not allowed to edit this venue')

    memberadd_form = VenueMemberAddForm()

    return object_list(request,
                       queryset=VenueMember.objects.filter(venue__id=venue.id),
                       template_name='venue/membership_manage.html',
                       template_object_name='venuemember',
                       extra_context={'venue': venue,
                                      'memberadd_form': memberadd_form}
                       )


@login_required
def membership_remove(request, venue_slug, member_id):
    """
    Remove a member from the venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)
    venuemember = get_object_or_404(VenueMember, venue=venue.id, user=member_id)

    # Permissions
    if not request.user.has_perm('venue.can_manage', venue):
        return HttpResponseForbidden(_("You are not allowed to edit this venue"))

    if len(venue.members.all()) == 1:
        messages.error(request, _("You can't let this venue alone"))
        return redirect('venue:membership-manage', venue.slug)

    # remove the permission
    remove_perm('venue.can_manage', venuemember.user, venue)
    
    return delete_object(request,
                         model=VenueMember,
                         object_id=venuemember.id,
                         template_name='venue/venuemember_confirm_delete.html',
                         template_object_name='venuemember',
                         post_delete_redirect=venuemember.get_absolute_url(),
                         extra_context={'venue': venue}
                         )

    
