from django.shortcuts import get_object_or_404

from band.models import Band
from venue.models import Venue
from bargain.views.generic import contract_new, contract_approve, contract_disapprove, contract_update, contract_detail

from ..models import GigBargain

def event_bargain_new(request, venue_slug):
    venue = get_object_or_404(Venue, slug=venue_slug)

    initial = {'venue': venue.id}
    formset_initial = []

    return contract_new(request,
                        aTermsClass=GigBargain,
                        initial=initial,
                        formset_initial=formset_initial,
                        post_create_redirect='event:bargain-detail'
                        )

def event_bargain_approve_band(request, band_slug, contract_id):
    """
    Approve view for a Band
    """
    band = get_object_or_404(Band, slug=band_slug)

    return contract_approve(request,
                            contract_id=contract_id,
                            aTermClass=GigBargain,
                            participant=band,
                            post_approve_redirect='event:bargain-detail'
                            )

def event_bargain_disapprove_band(request, band_slug, contract_id):
    """
    Disapprove view for a Band
    """
    band = get_object_or_404(Band, slug=band_slug)

    return contract_disapprove(request,
                               contract_id=contract_id,
                               aTermClass=GigBargain,
                               participant=band,
                               post_disapprove_redirect='event:bargain-detail'
                               )

def event_bargain_approve_venue(request, venue_slug, contract_id):
    """
    Approve view for a Venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    return contract_approve(request,
                            contract_id=contract_id,
                            aTermClass=GigBargain,
                            participant=venue,
                            post_approve_redirect='event:bargain-detail'
                            )

def event_bargain_disapprove_venue(request, venue_slug, contract_id):
    """
    Disapprove view for a Venue
    """
    venue = get_object_or_404(Venue, slug=venue_slug)

    return contract_disapprove(request,
                               contract_id=contract_id,
                               aTermClass=GigBargain,
                               participant=venue,
                               post_disapprove_redirect='event:bargain-detail'
                               )

def event_bargain_update(request, participant, contract_id):
    response = contract_update(request,
                               contract_id=contract_id,
                               aTermClass=GigBargain,
                               participant=participant,
                               post_update_redirect='event:bargain-detail')

    return response


def event_bargain_update_venue(request, venue_slug, contract_id):
    venue = get_object_or_404(Venue, slug=venue_slug)

    return event_bargain_update(request, venue, contract_id)

def event_bargain_update_band(request, band_slug, contract_id):
    band = get_object_or_404(Band, slug=band_slug)

    return event_bargain_update(request, band, contract_id)


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


