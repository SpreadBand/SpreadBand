from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.generic.create_update import update_object

from badges.models import Badge

from visitors.utils import record_visit

from .models import PressKit
from .forms import PressKitVideoForm
from .signals import presskitview_new, presskitview_band_comment, presskitview_venue_comment

@login_required
def presskit_detail(request, band_slug, template_name='presskit/presskit_detail.html'):
    presskit = get_object_or_404(PressKit, band__slug=band_slug)

    # Five latest gigs
    latest_gigs = presskit.band.gigs.past_events()[:5]
    
    extra_context = {'band': presskit.band,
                     'presskit': presskit,
                     'latest_gigs': latest_gigs}

    # If we are not in the band, record us as a visitor
    if not request.user in presskit.band.members.all():
        # Bands
        for band in request.user.bands.all():
            record_visit(band, presskit.band)

        # Venues
        for venue in request.user.venues.all():
            record_visit(venue, presskit.band)

    # Check if we can edit this presskit
    can_edit = request.user.has_perm('band.can_manage', presskit.band)

    # Completion badge
    presskit_completion_badge = Badge.objects.get(id='presskitcompletion')

    return render_to_response(template_name=template_name,
                              dictionary={'can_edit': can_edit,
                                          'presskit_completion_badge': presskit_completion_badge},
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )

@login_required
def mypresskit(request, band_slug):
    return presskit_detail(request,
                           band_slug,
                           'presskit/mypresskit.html')
    


from .models import PresskitViewRequest
from .forms import PresskitViewRequestForm
from django.utils.translation import ugettext as _
from django.contrib import messages
from venue.models import Venue


## XXX: Security
## XXX: Quota
## XXX: Notifications
@login_required
def presskit_send(request, band_slug, venue_slug):
    presskit = get_object_or_404(PressKit, band__slug=band_slug)
    venue = get_object_or_404(Venue, slug=venue_slug)
    band = presskit.band

    presskit_view_request_form = PresskitViewRequestForm(request.POST or None)

    if presskit_view_request_form.is_valid():
        view_request = PresskitViewRequest(presskit=presskit,
                                           venue=venue,
                                           sent_by=request.user)

        view_request.save()

        # Notify
        presskitview_new.send(sender=view_request)

        messages.success(request, _("%(band_name)s presskit was sent to %(venue_name)s") % {'band_name': band.name,
                                                                                            'venue_name': venue.name}
                         )

        return redirect(venue)

    return render_to_response(template_name='presskit/presskit_send.html',
                              dictionary={'venue': venue,
                                          'band': band,
                                          'presskit_view_request_form': presskit_view_request_form},
                              context_instance=RequestContext(request)
                              )

## XXX Security
@login_required
def presskit_viewrequest_band(request, band_slug, viewrequest_id):
    viewrequest = get_object_or_404(PresskitViewRequest, presskit__band__slug=band_slug, pk=viewrequest_id)

    # if there was news, mark it no more
    has_news = False
    if viewrequest.news_for_band:
        viewrequest.news_for_band = False
        has_news = True
        viewrequest.save()
    
    return render_to_response(template_name='presskit/presskit_viewrequest_band.html',
                              dictionary={'venue': viewrequest.venue,
                                          'band': viewrequest.presskit.band,
                                          'presskit': viewrequest.presskit,
                                          'has_news': has_news,
                                          'viewrequest': viewrequest},
                              context_instance=RequestContext(request)
                              )

@login_required
def presskit_viewrequest_band_comment(request, band_slug, viewrequest_id):
    viewrequest = get_object_or_404(PresskitViewRequest, presskit__band__slug=band_slug, pk=viewrequest_id)
    presskitview_band_comment.send(sender=viewrequest)
    return redirect('presskit:presskit-viewrequest-band', band_slug, viewrequest_id)


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
    

# XXX Security
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

