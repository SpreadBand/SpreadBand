__all__ = ['band', 'venue', 'dashboard']

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from event.models import GigBargain

from reversion.models import Version

from utils.differs import DictDiffer


def gigbargain_detail(request, gigbargain_uuid):
    """
    Get details about a Gig Bargain
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

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
    from collections import defaultdict
    from datetime import datetime, timedelta
    from django.db.models import Min, Max, F
    timeline = defaultdict(list)
    day = gigbargain.date
    first_gig = gigbargain.gigbargainband_set.filter(starts_at__isnull=False).order_by('starts_at')[0]
    last_gig = gigbargain.gigbargainband_set.filter(starts_at__isnull=False).order_by('-starts_at')[0]

    # Get global info
    global_start = datetime.combine(day, first_gig.starts_at)
    global_end = datetime.combine(day, last_gig.starts_at) + (last_gig.set_duration or timedelta(seconds=0))

    # Get info on all bands
    for gigbargainband in gigbargain.gigbargainband_set.all().order_by('starts_at'):
        if gigbargainband.starts_at and gigbargainband.set_duration:
            print first_gig.band.name, global_start, datetime.combine(day, gigbargainband.starts_at)
            timeline['bands'].append({'band': gigbargainband.band,
                                      'start': datetime.combine(day, gigbargainband.starts_at),
                                      'delta_start': datetime.combine(day, gigbargainband.starts_at) - global_start,
                                      'duration': gigbargainband.set_duration,
                                      'end': datetime.combine(day, gigbargainband.starts_at) + gigbargainband.set_duration
                                      })

    # Update global end in case the timeline is wrong
    for gig in timeline['bands']:
        if gig['end'] > global_end:
            global_end = gig['end']

    global_duration = global_end - global_start
    timeline['global'] = {'start': global_start,
                          'end': global_end, 
                          'duration': global_duration,
                          'steps': [global_start+timedelta(minutes=30*i) for i in range(0, global_duration.seconds / 60.0 / 30.0)], # Every 30min
                          }


    extra_context = {'gigbargain': gigbargain,
                     'old_versions': old_versions,
                     'timeline': timeline}



    return render_to_response(template_name='event/gigbargain_detail.html',
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )





from event.models import GigBargainCommentThread

def comments_section_display(request, gigbargain_uuid, section):
    """
    Display comments for a given gig bargain section
    """
    # XXX: Should limit sections
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)
    comment_thread, created = GigBargainCommentThread.objects.get_or_create(gigbargain=gigbargain,
                                                                            section=section)

    extra_context = {'gigbargain': gigbargain,
                     'comment_thread': comment_thread}

    return render_to_response(template_name='event/gigbargain_comments_section_display.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )


