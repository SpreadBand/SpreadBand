from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from band.models import Band

from .models import PressKit

def presskit_detail(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    # Five latest gigs
    latest_gigs = band.gigs.past_events()[:5]
    
    extra_context = {'band': band,
                     'latest_gigs': latest_gigs}

    return render_to_response(template_name='presskit/presskit_detail.html',
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )
