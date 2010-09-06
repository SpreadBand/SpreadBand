from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from .models import PressKit

def presskit_detail(request, band_slug, template_name='presskit/presskit_detail.html'):
    presskit = get_object_or_404(PressKit, band__slug=band_slug)

    # Five latest gigs
    latest_gigs = presskit.band.gigs.past_events()[:5]
    
    extra_context = {'band': presskit.band,
                     'presskit': presskit,
                     'latest_gigs': latest_gigs}

    return render_to_response(template_name=template_name,
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )

def mypresskit(request, band_slug):
    return presskit_detail(request,
                           band_slug,
                           'presskit/mypresskit.html')
    
