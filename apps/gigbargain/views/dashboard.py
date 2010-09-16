from calendar import HTMLCalendar
from collections import defaultdict

from datetime import datetime, date

from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from actstream.models import Action
from notification.models import Notice

from apps.band.models import Band
from apps.venue.models import Venue

from ..models import GigBargain


class GigBargainMonthlyHTMLCalendar(HTMLCalendar):
    """
    An HTML calendar for gigbargains of a given month
    """
    def __init__(self, firstweekday, aQueryset, when):
        HTMLCalendar.__init__(self, firstweekday)

        # Prepare a date-indexed list of gigbargains
        # XXX Maybe it's possible to do it using a query, but I don't know how
        self._gigbargains = defaultdict(list)
        for gigbargain in aQueryset:
            self._gigbargains[gigbargain.date].append(gigbargain)

        self._when = when

        self.today = date.today()
        
    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            the_day = date(self._when.year, self._when.month, day)
            css_classes = []
            css_classes.append(self.cssclasses[weekday])

            # Past date ?
            if the_day < self.today:
                css_classes.append('past')
            elif the_day == self.today:
                css_classes.append('today')
            
            infotip = ""
            # If there's a bargain
            if the_day in self._gigbargains:
                gigbargain = self._gigbargains[the_day][0]
                css_classes.append('cal-bargain-day')
                infotip = """<div class="cal-gb-info"><a href="%s">%s</a></div>""" % (gigbargain.get_absolute_url(),
                                                                                      gigbargain.venue.name)
                css_classes.append("infotip")

            res = ""
            for css_class in css_classes:
                res += " " + css_class
            return '<td class="%s">%d %s</td>' % (res, day, infotip)

    def toHTML(self):
        return self.formatmonth(self._when.year, self._when.month)


@login_required
def gigbargain_band_dashboard(request, band_slug):
    """
    The dashboard for a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    # retrieve notices
    notices_new = Notice.objects.notices_for(request.user).filter(notice_type__label='gigbargain_new')

    # Check date filters
    if request.GET.has_key('from'):
        date_from = datetime.strptime(request.GET['from'], '%Y-%m-%d')
    else:
        date_from = date.today

    date_to = None
    if request.GET.has_key('to'):
        date_to = datetime.strptime(request.GET['to'], '%Y-%m-%d')

    # retrieve gigbargains 
    # new_gigbargains = band.gigbargains.new_gigbargains().filter(date__gte=date_from)
    #new_gigbargains = band.gigbargains.filter(date__gte=date_from).filter(gigbargainband__in=band.gigbargainbands.filter(state='waiting')).order_by('date')
    new_gigbargains = band.gigbargains.draftsFor(band).filter(date__gte=date_from) | band.gigbargains.invitationsFor(band).filter(date__gte=date_from)
    if date_to:
        new_gigbargains = new_gigbargains.filter(date__lte=date_to)

    inprogress_gigbargains = band.gigbargains.inprogress_gigbargains().filter(date__gte=date_from).order_by('date')
    if date_to:
        inprogress_gigbargains = inprogress_gigbargains.filter(date__lte=date_to)

    concluded_gigbargains = band.gigbargains.concluded_gigbargains().filter(date__gte=date_from).order_by('date')
    if date_to:
        concluded_gigbargains = concluded_gigbargains.filter(date__lte=date_to)

    # Get all gigbargains of month
    when = date.today()
    month_gigbargains = band.gigbargains.filter(date__year=when.year, date__month=when.month).order_by('date')

    # Monthly calendar
    calendar = GigBargainMonthlyHTMLCalendar(firstweekday=0,
                                             aQueryset=month_gigbargains,
                                             when=when)

    # Monthly stats
    monthly_stats = {}
    monthly_stats['new'] = band.gigbargains.new_gigbargains().filter(date__year=when.year, date__month=when.month).count()
    monthly_stats['inprogress'] = band.gigbargains.inprogress_gigbargains().filter(date__year=when.year, date__month=when.month).count()
    monthly_stats['concluded'] = band.gigbargains.concluded_gigbargains().filter(date__year=when.year, date__month=when.month).count()
    monthly_stats['total'] = monthly_stats['new'] + monthly_stats['inprogress'] + monthly_stats['concluded']

    # Monthly connections
    monthly_connections = {}
    monthly_connections['bands'] = Band.objects.filter(gigbargains__in=month_gigbargains).exclude(pk=band).distinct()
    monthly_connections['venues'] = Venue.objects.filter(gigbargains__in=month_gigbargains).distinct()
    
    # Yearly graph
    yearly_stats = {}
    yearly_stats['new'] = band.gigbargains.new_gigbargains().extra(select={'month': "EXTRACT(month FROM date)"}).values('month').annotate(gigbargain_count=Count('pk'))
    yearly_stats['inprogress'] = band.gigbargains.inprogress_gigbargains().extra(select={'month': "EXTRACT(month FROM date)"}).values('month').annotate(gigbargain_count=Count('pk'))
    yearly_stats['concluded'] = band.gigbargains.concluded_gigbargains().extra(select={'month': "EXTRACT(month FROM date)"}).values('month').annotate(gigbargain_count=Count('pk'))

    yearly_values = {}
    import time
    for i in range(1, 13):
        month = date(year=date.today().year, month=i, day=1)
        ts = int(time.mktime(month.timetuple()))
        yearly_values[i] = {'new': 0, 'inprogress': 0, 'concluded': 0, 'label': month, 'ts': ts}

    for el in yearly_stats['new']:
        yearly_values[int(el['month'])]['new'] = el['gigbargain_count']

    for el in yearly_stats['inprogress']:
        yearly_values[int(el['month'])]['inprogress'] = el['gigbargain_count']

    for el in yearly_stats['concluded']:
        yearly_values[int(el['month'])]['concluded'] = el['gigbargain_count']

    # Get 10 latest actions
    latest_activity = Action.objects.stream_for_model(GigBargain).filter(target_object_id__in=inprogress_gigbargains|new_gigbargains)[:10]

    extra_context = {'band': band,
                     'notices_new': notices_new,
                     'latest_activity': latest_activity,
                     'new_gigbargains': new_gigbargains,
                     'inprogress_gigbargains': inprogress_gigbargains,
                     'concluded_gigbargains': concluded_gigbargains,
                     'monthly_calendar': calendar,
                     'monthly_stats': monthly_stats,
                     'monthly_connections': monthly_connections,
                     'yearly_stats': yearly_stats,
                     'yearly_values': yearly_values}

    return render_to_response(template_name='gigbargain/gigbargain_band_dashboard.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )




