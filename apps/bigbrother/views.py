
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from django.shortcuts import render_to_response

from django.http import HttpResponse

from .models import BandStatsDaily

from django.views.decorators.cache import cache_page

def show(request):
    return render_to_response('bigbrother/show.html')

from django.contrib.sites.models import Site
import settings

from django.db.models import Avg, Max, Min, Count, Sum
from datetime import datetime, date
from datetime import timedelta

from collections import defaultdict

import calendar

def make_monthly_graph(request):
    today = date.today()

    site = Site.objects.get(id=settings.SITE_ID)
    data_set = BandStatsDaily.objects.filter(site=site)

    first_day = date(today.year, today.month, 1)
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    last_day = date(today.year, today.month, days_in_month)

    return make_graph_range(data_set,
                            start=first_day,
                            end=last_day,
                            resolution='monthly'
                            )

def make_yearly_graph(request):
    today = date.today()

    site = Site.objects.get(id=settings.SITE_ID)
    data_set = BandStatsDaily.objects.filter(site=site)

    first_month = date(today.year, 1, 1)
    last_month = date(today.year, 12, 31)
        
    return make_graph_range(data_set,
                            start=first_month,
                            end=last_month,
                            resolution='yearly'
                            )
    

#@cache_page(60)
def make_graph_range(aDailyStatsSet,
                     start=None,
                     end=None,
                     resolution=None):

    if start:
        aDailyStatsSet = aDailyStatsSet.filter(date__gte=start)
        
    if end:
        aDailyStatsSet = aDailyStatsSet.filter(date__lte=end)

    delta = end - start

    if resolution == 'yearly':
        disc = '%%m'
        days = range(1, 12+1)
        
    elif resolution == 'monthly':
        disc = '%%d'
        days = range(1, delta.days+1)
        

    aDailyStatsSet = aDailyStatsSet.extra(select={"resolution": "strftime('%s', date)" % disc}).values("resolution").annotate(Sum("count")).order_by("resolution")

    data = defaultdict(int)
    for d in aDailyStatsSet:
        print d
        data[int(d['resolution'])] = d['count__sum']

    plt.figure(figsize=(10, 3))
    
    # graph code
    plt.plot(days, [data[d] for d in days], 'r-', label="user count")
    # the the x limits to the 'days' limit
    plt.xlim(1, len(days))
    # set the X ticks every 5 days
    plt.xticks(range(1, len(days)+1, 1))

    plt.ylim(0)
    plt.yticks(range(plt.ylim()[0], plt.ylim()[1], 1))

    # draw a grid
    plt.grid()
    
    # set title, X/Y labels
    plt.title(resolution)
    plt.xlabel("Days")
    plt.ylabel("user count")

    plt.legend()

    response = HttpResponse(content_type='image/png')
    plt.savefig(response)

    return response

