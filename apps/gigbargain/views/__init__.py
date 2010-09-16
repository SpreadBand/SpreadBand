__all__ = ['band', 'venue', 'dashboard']

from collections import defaultdict

from datetime import datetime, timedelta

from django.db.models import Min, Max, F
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from actstream.models import Action
from reversion.models import Version

from utils.differs import DictDiffer

from ..models import GigBargain, GigBargainCommentThread

@login_required
def gigbargain_detail(request, gigbargain_uuid):
    """
    Get details about a Gig Bargain
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    # Get bands we're allowed to manage
    managed_bands = []
    for band in gigbargain.gigbargainband_set.concurring():
        if request.user.has_perm('band.can_manage', band.band):
            managed_bands.append(band)

    # Check if we managed this venue
    is_venue_managed = request.user.has_perm('venue.can_manage', gigbargain.venue)

    # If we don't manage any of these bands and we're not the venue,
    # then forbid access
    if not len(managed_bands) and not is_venue_managed:
        return HttpResponseForbidden()

    # Compute changes between two latest revisions
    # XXX: Can be optimized, cached, ...
    old_versions = Version.objects.get_for_object(gigbargain)
    
    changes = {}
    max = len(old_versions)
    if max >= 2:
        old_version = old_versions[max-2]
        new_version = old_versions[max-1]
    
        d = DictDiffer(old_version.field_dict,
                       new_version.field_dict)

        for change in d.changed():
            changes[change] = (old_version.field_dict[change], new_version.field_dict[change])
    
    # Take care of the timeline
    timeline = defaultdict(list)
    day = gigbargain.date
    try:
        first_gig = gigbargain.gigbargainband_set.filter(starts_at__isnull=False).order_by('starts_at')[0]
        last_gig = gigbargain.gigbargainband_set.filter(starts_at__isnull=False).order_by('-starts_at')[0]
    except IndexError:
        first_gig = last_gig = None

    if first_gig and last_gig:
        # Get global info
        global_start = datetime.combine(day, first_gig.starts_at)
        global_end = datetime.combine(day, last_gig.starts_at) + (last_gig.set_duration or timedelta(seconds=0))

        # Get info on all bands
        for gigbargainband in gigbargain.gigbargainband_set.all().order_by('starts_at'):
            if gigbargainband.starts_at and gigbargainband.set_duration:
                timeline['bands'].append({'band': gigbargainband.band,
                                          'start': datetime.combine(day, gigbargainband.starts_at),
                                          'delta_start': datetime.combine(day, gigbargainband.starts_at) - global_start,
                                          'duration': gigbargainband.set_duration,
                                          'end': datetime.combine(day, gigbargainband.starts_at) + gigbargainband.set_duration
                                          })

        # Update global end in case the timeline is wrong
        # and also compute time between two gigs
        previous_gig = None
        for gig in timeline['bands']:
            if gig['end'] > global_end:
                global_end = gig['end']

            if previous_gig:
                time_between = gig['start'] - previous_gig['end']
                gig['time_before_previous'] = time_between

            previous_gig = gig

        global_duration = global_end - global_start
        timeline['global'] = {'start': global_start,
                              'end': global_end, 
                              'duration': global_duration,
                              'steps': [global_start+timedelta(minutes=30*i) for i in range(0, global_duration.seconds / 60 / 30)], # Every 30min
                              }

    latest_activity = Action.objects.stream_for_model(GigBargain).filter(target_object_id=gigbargain.id)[:10]


    # Progress bar indicator for gigbargain macro state
    if gigbargain.macro_state == 'draft':
        gigbargain_mstate = 0
    elif gigbargain.macro_state == 'submitted':
        gigbargain_mstate = 1
    elif gigbargain.macro_state == 'negociations':
        gigbargain_mstate = 2
    elif gigbargain.macro_state == 'finished':
        gigbargain_mstate = 3

    # Get comment objects for every section
    comments = dict()
    for section in ("whenwhere", "access", "timeline", "remuneration", "defrayments"):
        comment_thread, created = GigBargainCommentThread.objects.get_or_create(gigbargain=gigbargain,
                                                                                section=section)
        comments[section] = comment_thread


    extra_context = {'gigbargain': gigbargain,
                     'gigbargain_mstate': gigbargain_mstate,
                     'managed_bands': managed_bands,
                     'is_venue_managed': is_venue_managed,
                     'old_versions': old_versions,
                     'timeline': timeline,
                     'latest_activity': latest_activity,
                     'comments': comments,
                     }

    return render_to_response(template_name='gigbargain/gigbargain_detail.html',
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )

from ..forms import SectionComment

def comments_section_display(request, gigbargain_uuid, section):
    """
    Display comments for a given gig bargain section
    """
    # XXX: Should limit sections
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    comment_thread, created = GigBargainCommentThread.objects.get_or_create(gigbargain=gigbargain,
                                                                            section=section)

    extra_context = {'gigbargain': gigbargain,
                     'comment_thread': comment_thread}

    return render_to_response(template_name='gigbargain/gigbargain_comments_section_display.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )


