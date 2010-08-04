from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

import agenda.views
from agenda.views.vobject_django import icalendar

from band.models import Band
from venue.models import Venue

from ..models import Gig
from ..forms import GigCreateForm

def gig_detail(request, year, month, day, slug):
    """
    Get details about a gig
    """
    return agenda.views.date_based.object_detail(request, 
                                                 Gig.objects.all(), 
                                                 'event_date',
                                                 year, month, day, slug, 
                                                 template_name='event/gig_detail.html', 
                                                 template_object_name='gig', 
                                                 )

def gig_create(request, band_slug):
    """
    Create an event of type gig and links it to any involved actor
    """
    requesting_band = get_object_or_404(Band, slug=band_slug)

    gigform = GigCreateForm(data=request.POST or None)

    if request.method == 'POST':
        if gigform.is_valid():
            # XXX: It seems that integrity cannot be checked before throwing an error.
            gig = gigform.save(commit=False)
            gig.creator = request.user
            gig.save()
            gigform.save_m2m()

            # Add this gig to the band calendar
            # XXX: Should save to every band involved, not only the creator.
            for band in gig.bands.all():
                band.calendar.events.add(gig)

            # Also add this gig to the venue calendar            
            gig.venue.calendar.events.add(gig)

            redirect(requesting_band)

    return render_to_response(template_name='event/create_event.html',
                              dictionary={'gigform': gigform},
                              context_instance=RequestContext(request)
                              )

from datetime import date

def gig_cancel(request, year, month, day, slug):
    gig_date = date(int(year), int(month), int(day))
    gig = get_object_or_404(Gig, event_date=gig_date, slug=slug)

    # Set to canceled
    gig.state = 'C'
    
    gig.save()

    return redirect(gig)

def gig_uncancel(request, year, month, day, slug):
    gig_date = date(int(year), int(month), int(day))
    gig = get_object_or_404(Gig, event_date=gig_date, slug=slug)

    # Set to canceled
    gig.state = 'V'
    
    gig.save()

    return redirect(gig)

            

from agenda.models import Calendar
from agenda.views import date_based
from agenda.views.timeline import timeline
from ..models import Gig

#XXX Bad hack
import imp
fp, pathname, description = imp.find_module('calendar')
pythoncal = imp.load_module('calendar', fp, pathname, description)
from collections import defaultdict

class GigMonthlyHTMLCalendar(pythoncal.HTMLCalendar):
    """
    An HTML calendar for gigs of a given month
    """
    def __init__(self, firstweekday, aQueryset, when):
        pythoncal.HTMLCalendar.__init__(self, firstweekday)

        # Prepare a date-indexed list of gigbargains
        # XXX Maybe it's possible to do it using a query, but I don't know how
        self._gigs = defaultdict(list)
        for gig in aQueryset:
            self._gigs[gig.event_date].append(gig)

        self._when = when
        
    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            the_day = date(self._when.year, self._when.month, day)
            if the_day in self._gigs:
                cell = '<td class="%s"><font color="red">%d</font>' % (self.cssclasses[weekday], day)
                cell += '<ul>'
                for gig in self._gigs[the_day]:
                    cell += '<li><a href="%s">%s</a></li>' % (gig.get_absolute_url(),
                                                              gig.title)
                cell += '</ul></td>'
                return cell
            else:
                return '<td class="%s">%d</td>' % (self.cssclasses[weekday], day)

    def toHTML(self):
        return self.formatmonth(self._when.year, self._when.month)


def band_calendar_detail(request, band_slug):
    """
    Show a calendar for a Band
    """
    band = get_object_or_404(Band, slug=band_slug)

    today = date.today()
    gigs = band.gigs.filter(event_date__year=today.year,
                            event_date__month=today.month)

    monthly_calendar = GigMonthlyHTMLCalendar(firstweekday=0,
                                              aQueryset=gigs,
                                              when=today)

    return timeline(request,
                    model=Gig,
                    calendar=band.calendar,
                    past_event_count=1,
                    template_name='event/band_timeline.html',
                    extra_context={'band': band,
                                   'monthly_calendar': monthly_calendar},
                    )

def band_calendar_ics(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    return icalendar(request,
                     queryset=band.calendar.events.all(),
                     date_field='event_date',
                     ical_filename='%s.ics' % band.slug,
                     last_modified_field='mod_field',
                     location_field='location',
                     start_time_field='start_time',
                     end_time_field='end_time')

def venue_calendar_ics(request, venue_slug):
    venue = get_object_or_404(Venue, slug=venue_slug)

    return icalendar(request,
                     queryset=venue.calendar.events.all(),
                     date_field='event_date',
                     ical_filename='%s.ics' % venue.slug,
                     last_modified_field='mod_field',
                     location_field='location',
                     start_time_field='start_time',
                     end_time_field='end_time')


def venue_calendar_detail(request, venue_slug):
    """
    Show a calendar for a Venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    return timeline(request,
                    model=Gig,
                    past_event_count=1,
                    calendar=venue.calendar,
                    template_name="event/venue_timeline.html",
                    extra_context={'venue': venue},
                    )

    

    
