from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

#from schedule.periods import Month
#from schedule.models import Calendar
#from schedule.views import create_or_edit_event, calendar_by_periods

from band.models import Band
from venue.models import Venue

from ..forms import GigCreateForm

def gig_create(request, band_slug):
    """
    Create an event of type gig and links it to any involved actor
    """
    band = get_object_or_404(Band, slug=band_slug)

    # calendar_slug = "band_%d" % band.id
    # calendar = Calendar.objects.get_or_create_calendar_for_object(band, name=calendar_slug)

    gigform = GigCreateForm(data=request.POST or None)

    if request.method == 'POST':
        if gigform.is_valid():
            gig = gigform.save(commit=False)
            #gig.creator = request.user
            #gig.calendar = calendar
            gig.save()
            
            # Also add this gig to the venue calendar
            # venue = gigform.cleaned_data['venue']
            # venue_slug = "venue_%d" % venue.id
            # venue_calendar = Calendar.objects.get_or_create_calendar_for_object(venue,
            #                                                                     name=venue_slug)
            # venue_calendar.events.add(gig)
            # venue_calendar.save()

            redirect(gig)

    return render_to_response(template_name='event/create_event.html',
                              dictionary={'gigform': gigform},
                              context_instance=RequestContext(request)
                              )
            

from agenda.models import Calendar
from agenda.views import date_based
from agenda.views.timeline import timeline
from ..models import Gig

def band_calendar_detail(request, band_slug):
    """
    Show a calendar for a Band
    """
    band = get_object_or_404(Band, slug=band_slug)

    return timeline(request,
                    model=Gig,
                    calendar=band.calendar,
                    template_name='event/calendar_by_period.html')

def venue_calendar_detail(request, venue_slug):
    """
    Show a calendar for a Venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    return timeline(request,
                    model=Gig,
                    calendar=venue.calendar,
                    template_name="event/calendar_by_period.html",
                    )

    

    
