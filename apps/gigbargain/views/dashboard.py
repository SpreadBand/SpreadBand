from calendar import HTMLCalendar
from collections import defaultdict

from datetime import datetime, date

from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from notification.models import Notice

from apps.band.models import Band

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
        
    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            the_day = date(self._when.year, self._when.month, day)
            if the_day in self._gigbargains:
                return '<td class="%s"><font color="red">%d</font></td>' % (self.cssclasses[weekday], day)
            else:
                return '<td class="%s">%d</td>' % (self.cssclasses[weekday], day)

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
    new_gigbargains = band.gigbargains.new_gigbargains().filter(date__gte=date_from)
    if date_to:
        new_gigbargains = new_gigbargains.filter(date__lte=date_to)

    inprogress_gigbargains = band.gigbargains.inprogress_gigbargains().filter(date__gte=date_from)
    if date_to:
        inprogress_gigbargains = inprogress_gigbargains.filter(date__lte=date_to)

    concluded_gigbargains = band.gigbargains.concluded_gigbargains().filter(date__gte=date_from)
    if date_to:
        concluded_gigbargains = concluded_gigbargains.filter(date__lte=date_to)

    # Get all gigbargains of month
    when = date.today()
    month_gigbargains = band.gigbargains.filter(date__year=when.year, date__month=when.month)

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
    
    # Yearly graph
    yearly_stats = {}
    yearly_stats['new'] = band.gigbargains.new_gigbargains().extra(select={'month': "EXTRACT(month FROM date)"}).values('month').annotate(gigbargain_count=Count('pk'))
    yearly_stats['inprogress'] = band.gigbargains.inprogress_gigbargains().extra(select={'month': "EXTRACT(month FROM date)"}).values('month').annotate(gigbargain_count=Count('pk'))
    yearly_stats['concluded'] = band.gigbargains.concluded_gigbargains().extra(select={'month': "EXTRACT(month FROM date)"}).values('month').annotate(gigbargain_count=Count('pk'))

    yearly_values = {}
    for i in range(1, 13):
        yearly_values[i] = {'new': 0, 'inprogress': 0, 'concluded': 0, 'label': date(year=date.today().year, month=i, day=1)}

    for el in yearly_stats['new']:
        yearly_values[int(el['month'])]['new'] = el['gigbargain_count']

    for el in yearly_stats['inprogress']:
        yearly_values[int(el['month'])]['inprogress'] = el['gigbargain_count']

    for el in yearly_stats['concluded']:
        yearly_values[int(el['month'])]['concluded'] = el['gigbargain_count']
    

    extra_context = {'band': band,
                     'notices_new': notices_new,
                     'new_gigbargains': new_gigbargains,
                     'inprogress_gigbargains': inprogress_gigbargains,
                     'concluded_gigbargains': concluded_gigbargains,
                     'monthly_calendar': calendar,
                     'monthly_stats': monthly_stats,
                     'monthly_connections': monthly_connections,
                     'yearly_stats': yearly_stats,
                     'yearly_values': yearly_values}

    return render_to_response(template_name='event/gigbargain_band_dashboard.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )




