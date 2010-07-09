__all__ = ['band', 'venue']

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from event.models import GigBargain

def gigbargain_detail(request, gigbargain_uuid):
    """
    Get details about a Gig Bargain
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

    old_versions = Version.objects.get_for_object(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'old_versions': old_versions}

    return render_to_response(template_name='event/gigbargain_detail.html',
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )


from reversion.models import Version
from bargain.models import Contract

from utils.differs import DictDiffer

def event_bargain_detail(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)


    # Compute changes between two latest revisions
    # XXX: Can be optimized, cached, ...
    available_versions = Version.objects.get_for_object_reference(GigBargain, contract.terms.id)
    
    changes = {}
    max = len(available_versions)
    if max >= 2:
        old_version = available_versions[max-2]
        new_version = available_versions[max-1]
    
        d = DictDiffer(old_version.field_dict,
                       new_version.field_dict)

        for change in d.changed():
            changes[change] = (old_version.field_dict[change], new_version.field_dict[change])

    return contract_detail(request,
                           aTermClass=GigBargain,
                           contract_id=contract_id,
                           extra_context={'changes' : changes})


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


