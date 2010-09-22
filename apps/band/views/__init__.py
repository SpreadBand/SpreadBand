from datetime import date

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

from geopy import geocoders

from guardian.shortcuts import assign

from world.models import Place

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
                band = create_form.save()
                
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
        return HttpResponseForbidden('You are not allowed to edit this band')


    if request.method == 'POST':
        band_form = BandUpdateForm(request.POST, request.FILES,
                                   instance=band)

        if band_form.is_valid():
            band = band_form.save(commit=False)
            g = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)
            try:
                geoplace, (lat, lng) = g.geocode('%s %s, %s' % (band.zipcode,
                                                                band.city,
                                                                band.country),
                                                 exactly_one=True,
                                                 )
            except ValueError, e:
                geoplace = _("Unable to find address")
                lat = lng = 0

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

            messages.success(request, "%s was successfully updated" % band.name)

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
    Redirect to the dashboard if manager of this band or send the
    viewer to the presskit
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if request.user.has_perm('band.can_manage', band):
        return redirect('band:dashboard', band.slug)
    else:
        return redirect('presskit:presskit-detail', band.slug)

# XXX: Security
@login_required
def dashboard(request, band_slug):
    """
    Show details about a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    past_events = band.gigs.past_events()[:1]
    future_events = band.gigs.future_events()[0:5]

    today_events = band.gigs.future_events().filter(event_date=date.today())

    # make a calendar
    from event.views.calendar import GigMonthlyHTMLCalendar
    monthly_calendar = GigMonthlyHTMLCalendar(firstweekday=0,
                                              aQueryset=band.gigs.all(),
                                              when=date.today())

    # gigbargains
    gigbargain_invitations = band.gigbargains.invitationsFor(band)
    gigbargain_drafts = band.gigbargains.draftsFor(band)

    # Get 5 latest gigbargain activities
    from actstream.models import Action
    from gigbargain.models import GigBargain
    latest_activity = Action.objects.stream_for_model(GigBargain).filter(target_object_id__in=band.gigbargains.inprogress_gigbargains())[:3]

    extra_context = {'past_events': past_events,
                     'future_events': future_events,
                     'today_events': today_events,
                     'monthly_calendar': monthly_calendar,
                     'latest_activity': latest_activity,
                     'gigbargain_invitations': gigbargain_invitations,
                     'gigbargain_drafts': gigbargain_drafts}

    return object_detail(request,
                         queryset=Band.objects.all(),
                         slug=band_slug,
                         template_object_name='band',
                         template_name='bands/band_detail.html',
                         extra_context=extra_context
                         )


    

#--- PICTURES

# XX: Security
@login_required
def picture_list(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    return object_list(request,
                       queryset=band.pictures.all(),
                       template_name='band/picture_list.html',
                       template_object_name='picture',
                       extra_context={'band': band},
                       )

# XX: Security
@login_required
def picture_new(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

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


# XXX: Security
@login_required
def picture_delete(request, band_slug, picture_id):
    band = get_object_or_404(Band, slug=band_slug)
    picture = get_object_or_404(band.pictures, id=picture_id)

    picture.delete()

    return redirect('band:band-pictures', band.slug)
