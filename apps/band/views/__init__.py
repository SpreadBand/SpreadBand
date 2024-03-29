# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import gettext as _
from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail

from tagging.models import TaggedItem
from geopy import geocoders

from actstream.models import Action
from badges.models import Badge
from guardian.shortcuts import assign
from visitors.utils import get_latest_visits_for

from event.views.calendar import GigMonthlyHTMLCalendar
# from gigbargain.models import GigBargain
from world.models import Place

from presskit.models import PresskitViewRequest

from ..models import Band, BandMember
from ..forms import BandCreateForm, BandUpdateForm
from ..forms import BandPictureForm, BandMemberRequestForm

@login_required
def new(request):
    """
    register a new band
    """
    create_form = BandCreateForm(request.POST or None)
    member_form = BandMemberRequestForm(request.POST or None)

    if request.method == 'POST':
        if member_form.is_valid():
            if create_form.is_valid():
                # Create the band
                band = create_form.save(commit=False)
                band.genres = ", ".join(request.POST.getlist('genres') or [])

                # Lookup Geo (duplicated from edit, fix this!)
                g = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)
                
                # Ugly hack to get a place from geocoders -_-
                where = u'%s %s, %s' % (band.zipcode,
                                        band.city,
                                        band.country.name)
                
                geoplace = _("Unable to lookup address")
                lat = lng = 0
                for match in g.geocode(where.encode('utf-8'),
                                       exactly_one=False):
                    geoplace, (lat, lng) = match
                    # Get the first result
                    break

                # Edit
                point = Point(lng, lat)
                if band.place:
                    place = band.place
                    place.address = geoplace
                    place.geom = point
                    place.save()
                else:
                    place = Place.objects.create(address=geoplace, geom=point)

                band.place = place

                band.save()
                
                # Add this user into the band
                bandmember = BandMember(band=band,
                                        user=request.user
                                        )
                bandmember.save()
                bandmember.roles = member_form.cleaned_data.get('roles')
                bandmember.save()
                
                # Assign rights to the user
                assign('band.can_manage', bandmember.user, band)
               
                return redirect(band)

    return render_to_response(template_name='bands/band_new.html',
                              dictionary={'form': create_form,
                                          'member_form': member_form},
                              context_instance=RequestContext(request)
                              )

@login_required
def edit(request, band_slug):
    """
    edit a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Check if we're allowed to edit this band
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden('You are not allowed to manage this band')


    if request.method == 'POST':
        band_form = BandUpdateForm(request.POST, request.FILES,
                                   instance=band)

        if band_form.is_valid():
            band = band_form.save(commit=False)
            band.genres = ", ".join(request.POST.getlist('genres') or [])

            # Lookup Geo
            g = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)

            # Ugly hack to get a place from geocoders -_-
            where = u'%s %s, %s' % (band.zipcode,
                                    band.city,
                                    band.country.name)

            geoplace = _("Unable to lookup address")
            lat = lng = 0
            for match in g.geocode(where.encode('utf-8'),
                                   exactly_one=False):
                geoplace, (lat, lng) = match
                # Get the first result
                break

            # Edit
            point = Point(lng, lat)
            if band.place:
                place = band.place
                place.address = geoplace
                place.geom = point
                place.save()
            else:
                place = Place.objects.create(address=geoplace, geom=point)

            band.place = place
            band.save()

            messages.success(request, _(u"%s was successfully updated" % band.name))

            return redirect('presskit:mypresskit', band.slug)


    return update_object(request,
                         form_class=BandUpdateForm,
                         slug=band_slug,
                         template_name='bands/band_update.html',
                         extra_context={'band': band},
                         )

                          
def list(request):
    """
    list all bands
    """
    return object_list(request,
                       queryset=Band.objects.all(),
                       template_name='bands/band_list.html',
                       template_object_name='band',
                       )

#-- events
def event_detail(request, band_slug):
    pass

def event_new(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    return create_object(request,
                         form_class=GigForm,
                         template_name='bands/event_new.html',
                         extra_context={'band': band}
                         )
    


def detail(request, band_slug):
    """
    Redirect to the dashboard if manager of this band or send the
    viewer to the presskit
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if request.user.has_perm('band.can_manage', band):
        return redirect('band:dashboard', band.slug)
    else:
        return redirect('presskit:presskit-detail', band.slug)


@login_required
def dashboard(request, band_slug):
    """
    Show details about a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden('You are not allowed to view this dashboard band')
    

    #past_events = band.gigs.past_events()[:1]
    #future_events = band.gigs.future_events()[0:5]

    #today_events = band.gigs.future_events().filter(event_date=date.today())

    # make a calendar
    #monthly_calendar = GigMonthlyHTMLCalendar(firstweekday=0,
    #                                          aQueryset=band.gigs.all(),
    #                                          when=date.today())

    # gigbargains
    #gigbargain_invitations = band.gigbargains.invitationsFor(band)
    #gigbargain_drafts = band.gigbargains.draftsFor(band)

    # Get 5 latest gigbargain activities
    # latest_activity = Action.objects.stream_for_model(GigBargain).filter(target_object_id__in=band.gigbargains.inprogress_gigbargains())[:3]

    # Get 10 latest visits
    latest_visits = get_latest_visits_for(band)

    # Presskit completion
    presskit_completion_badge = Badge.objects.get(id='presskitcompletion')

    presskit_completion = dict()
    presskit_completion['perc'] = int(presskit_completion_badge.meta_badge.get_progress_percentage(band))

    condition_callbacks = [getattr(presskit_completion_badge.meta_badge, c) for c in dir(presskit_completion_badge.meta_badge) if c.startswith('check')]
    for fn in condition_callbacks:
        presskit_completion[fn.__name__] = fn(band)

    # Presskit tracker
    show_pktracker_history = request.GET.get('pktracker_history', False) # Switch if we need to show *all* gig requests or limited history

    if not show_pktracker_history:
        # Show either 30 latest days or the latest 15 presskits
        ten_days_ago = datetime.now() - timedelta(days=30)

        sent_presskits = PresskitViewRequest.objects.filter(presskit=band.presskit, 
                                                            modified_on__gte=ten_days_ago).order_by('modified_on', '-sent_on', 'state')[:15]
    else:
        # Show 50 latest presskits
        sent_presskits = PresskitViewRequest.objects.filter(presskit=band.presskit).order_by('modified_on', '-sent_on', 'state')[:50]


    extra_context = {#'past_events': past_events,
                     #'future_events': future_events,
                     #'today_events': today_events,
                     #'monthly_calendar': monthly_calendar,
                     # 'latest_activity': latest_activity,
                     #'gigbargain_invitations': gigbargain_invitations,
                     #'gigbargain_drafts': gigbargain_drafts,
                     'latest_visits': latest_visits,
                     'presskit_completion': presskit_completion,
                     'presskit_completion_badge': presskit_completion_badge,
                     'sent_presskits': sent_presskits}

    return object_detail(request,
                         queryset=Band.objects.all(),
                         slug=band_slug,
                         template_object_name='band',
                         template_name='bands/band_detail.html',
                         extra_context=extra_context
                         )


    

#--- PICTURES
@login_required
def picture_list(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden('You are not allowed to manage this band')

    return object_list(request,
                       queryset=band.pictures.all(),
                       template_name='band/picture_list.html',
                       template_object_name='picture',
                       extra_context={'band': band},
                       )

@login_required
def picture_new(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden('You are not allowed to manage this band')

    if request.method == 'POST':
        picture_form = BandPictureForm(request.POST, request.FILES)

        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.band = band

            picture.save()

            return redirect('band:band-pictures', band.slug)

    return create_object(request,
                         form_class=BandPictureForm,
                         template_name='bands/picture_new.html',
                         extra_context={'band': band}
                         )


@login_required
def picture_delete(request, band_slug, picture_id):
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden('You are not allowed to manage this band')

    picture = get_object_or_404(band.pictures, id=picture_id)

    picture.delete()

    return redirect('band:band-pictures', band.slug)


from ..filters import BandFilter

from geopy import geocoders
from django.utils.translation import gettext as _
from django.contrib.gis.measure import D
from django.core.paginator import Paginator

from ..forms import BandGeoSearchForm

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


@login_required
def search(request):
    # Reconstruct the ambiance list since we use a multivariable trick
    genres_tags = request.GET.getlist("genres") or []

    band_filter = BandFilter(request.GET, queryset=Band.objects.all())


    # Try to find the default place
    default_country = None
    default_city = None
    
    if request.user.get_profile().town and request.user.get_profile().country: 
        default_city = request.user.get_profile().town
        default_country = request.user.get_profile().country

    elif len(request.user.bands.all()) == 1:
        band = request.user.bands.all()[0]
        if band.city and band.country:
            default_country = band.country
            default_city = band.city

    elif len(request.user.venues.all()) == 1:
        venue = request.user.venues.all()[0]
        if venue.city and venue.country:
            default_city = venue.city
            default_country = venue.country

    geosearch_form = BandGeoSearchForm(request.GET or {'country': default_country,
                                                       'city': default_city})
    
    if geosearch_form.is_valid():
        city = geosearch_form.cleaned_data.get('city')
        country = geosearch_form.cleaned_data.get('country')
        distance = geosearch_form.cleaned_data.get('distance')

        # If we have a distance, do a geo lookup
        if distance and city and country:
            try:
                point = lookup_place(city, countries.OFFICIAL_COUNTRIES[country])
            except geocoders.google.GQueryError, e:
                geosearch_form.errors['city'] = _('Unable to find this city. Check the country or be more specific.')
            else:
                places = Place.objects.filter(geom__distance_lte=(point, D(km=distance)))
                band_filter.queryset = band_filter.queryset.filter(place__in=places.all())
        # Otherwise, try to match by name
        else:
            if city:
                band_filter.queryset = band_filter.queryset.filter(city__iexact=city)
            if country:
                band_filter.queryset = band_filter.queryset.filter(country__iexact=country)

        # Restrict by filtering by genre
        if genres_tags:
            # Filter bands that match one of these tags
            band_filter.queryset = TaggedItem.objects.get_union_by_model(band_filter.queryset, genres_tags)


    return render_to_response(template_name='band/band_search.html',
                              dictionary={'band_filter': band_filter,
                                          'geosearch_form': geosearch_form,
                                          'genres_tags': genres_tags},
                              context_instance=RequestContext(request)
                              )
