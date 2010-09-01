from datetime import date

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail

from geopy import geocoders

from world.models import Place

from ..models import Band
from ..forms import BandCreateForm, BandUpdateForm
from ..forms import BandPictureForm

@login_required
def new(request):
    """
    register a new band
    """
    return create_object(request,
                         form_class=BandCreateForm,
                         template_name='bands/band_new.html',
                         )

@login_required
def edit(request, band_slug):
    """
    edit a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Check if we're allowed to edit this band
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden('You are not allowed to edit this band')


    if request.method == 'POST':
        band_form = BandUpdateForm(request.POST, request.FILES,
                                   instance=band)

        if band_form.is_valid():
            band = band_form.save(commit=False)
            g = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)
            geoplace, (lat, lng) = g.geocode('%s %s, %s' % (band.zipcode,
                                                            band.city,
                                                            band.country),
                                             exactly_one=True,
                                             )

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

            return redirect(band)


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
    Show details about a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    past_events = band.gigs.past_events()[:1]
    future_events = band.gigs.future_events()[0:5]

    today_events = band.gigs.future_events().filter(event_date=date.today())

    extra_context = {'past_events': past_events,
                     'future_events': future_events,
                     'today_events': today_events}

    return object_detail(request,
                         queryset=Band.objects.all(),
                         slug=band_slug,
                         template_object_name='band',
                         template_name='bands/band_detail.html',
                         extra_context=extra_context
                         )


    

#--- PICTURES
def picture_new(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    if request.method == 'POST':
        picture_form = BandPictureForm(request.POST, request.FILES)

        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.band = band

            picture.save()

            return redirect(band)

    return create_object(request,
                         form_class=BandPictureForm,
                         template_name='bands/picture_new.html',
                         extra_context={'band': band}
                         )
