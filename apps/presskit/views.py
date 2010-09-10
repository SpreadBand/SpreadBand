from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.generic.create_update import update_object

from .models import PressKit
from .forms import PressKitVideoForm

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
    


## XXX: Security
@login_required
def video_edit(request, band_slug):
    presskit = get_object_or_404(PressKit, band__slug=band_slug)
    
    return update_object(request,
                         template_name='presskit/video_edit.html',
                         template_object_name='presskit',
                         object_id=presskit.id,
                         form_class=PressKitVideoForm)
    

#-- TRACKS --#
from django.views.generic.create_update import create_object, delete_object
from django.views.generic.list_detail import object_list

from media.models import Track
from .forms import PressKitTrackForm

# XXX Security
@login_required
def track_add(request, band_slug):
    presskit = get_object_or_404(PressKit, band__slug=band_slug)

    track_form = PressKitTrackForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if track_form.is_valid():
            track = track_form.save()
            
            presskit.tracks.add(track)
            presskit.save()
            
            return redirect('presskit:presskit-tracks', presskit.band.slug)

    return create_object(request,
                         model=Track,
                         template_name='presskit/track_add.html',
                         extra_context={'presskit': presskit},
                         )
    

# XXX Seucrity
@login_required
def track_list(request, band_slug):
    presskit = get_object_or_404(PressKit, band__slug=band_slug)

    return object_list(request,
                       queryset=presskit.tracks.all(),
                       template_name='presskit/track_list.html',
                       template_object_name='track',
                       extra_context={'presskit': presskit}
                       )

# XXX: Security
@login_required
def track_delete(request, band_slug, track_id):
    presskit = get_object_or_404(PressKit, band__slug=band_slug)
    track = get_object_or_404(presskit.tracks, id=track_id)

    track.delete()

    return redirect('presskit:presskit-tracks', presskit.band.slug)

