from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

from django.template.loader import render_to_string

from django.contrib.gis.geos import Point

from .forms import VenueGeoSearchForm
from .views import search_venue_atomic

def search_venues(request, form_data):
    dajax = Dajax()

    print form_data

    geosearch_form = VenueGeoSearchForm(form_data)

    if geosearch_form.is_valid():
        distance = geosearch_form.cleaned_data.get('distance')
        circle_x = geosearch_form.cleaned_data.get('circle_x')
        circle_y = geosearch_form.cleaned_data.get('circle_y')

        center_point = Point(circle_x, circle_y)
        venue_filter = search_venue_atomic(form_data, center_point, distance, form_data.get('ambiance') or [])
        
        render = render_to_string(template_name='venue/search_results.html',
                                  dictionary={'venue_filter': venue_filter},
                                  context_instance=RequestContext(request)
                                  )

    else:
        render = render_to_string(template_name='venue/search_results.html',
                                  dictionary={'venue_filter': []},
                                  context_instance=RequestContext(request)
                                  )
        
    dajax.assign('#search-results-wrapper', 'innerHTML', render)

    return dajax.json()

dajaxice_functions.register(search_venues)




