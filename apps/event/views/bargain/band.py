from datetime import timedelta

from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from durationfield.utils.timestring import from_timedelta
import notification.models as notification

from apps.band.models import Band
from apps.venue.models import Venue

from event.models import GigBargain, GigBargainBand
from event.forms import GigBargainBandPartEditForm

def gigbargain_enter_for_band(request, band_slug, gigbargain_uuid):
    """
    Enter a bargain, for a band
    """
    band = get_object_or_404(Band, slug=band_slug)
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

    gigbargain_band = get_object_or_404(GigBargainBand, 
                                        bargain__pk=gigbargain_uuid,
                                        band__slug=band_slug)
    
    # XXX Should check that contract state is "new"

    # If we were waiting, switch to "accepted" and save
    if gigbargain_band.state == 'waiting':
        gigbargain_band.accept()

        messages.success(request, _("You (%s) are now bargaining with %s") % (band.name,
                                                                              gigbargain.venue.name)
                         )

        # If everybody has accepted, bands can start negociating
        if all([gigbargain_band.state == 'accepted' for gigbargain_band in gigbargain.gigbargainband_set.all()]):
            for gigbargain_band in gigbargain.gigbargainband_set.all():
                gigbargain_band.start_negociating()

            # Then, update bargain state
            gigbargain.start_band_negociation()

        
        # If /SOME/ of the bands have accepted, ask the venue if we start negociation or not
        elif all([gigbargain_band.state != 'waiting' for gigbargain_band in gigbargain.gigbargainband_set.all()]):
            gigbargain.need_venue_confirmation()
            

    # If not, warn we have already entered the bargain
    elif gigbargain_band.state in ('accepted', 'negociating', 'validated'):
        messages.warning(request, _("You (%s) are already bargaining with %s") % (band.name,
                                                                                  gigbargain.venue.name)
                         )

    # If we're no more in the bargain
    elif gigbargain_band.state in ('refused', 'exited', 'kicked'):
        messages.error(request, _("You are no more part of this bargain"))

    return redirect(gigbargain)


# XXX: beware of state : should be more constrained
def gigbargain_refuse_for_band(request, band_slug, gigbargain_uuid):
    """
    For a Band, don't enter a gigbargain and so refuse it.
    """
    band = get_object_or_404(Band, slug=band_slug)
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

    gigbargain_band = get_object_or_404(GigBargainBand, 
                                        bargain__pk=gigbargain_uuid,
                                        band__slug=band_slug)
    
    # If we were waiting, switch to "refused" and save
    if gigbargain_band.state == 'waiting':
       gigbargain_band.refuse()

       # No more bands are waiting, trigger bargain state update
       if all([gigbargain_band.state != 'waiting' for gigbargain_band in gigbargain.gigbargainband_set.all()]):
           gigbargain.need_venue_confirmation()

       messages.success(request, _("You (%s) have refused to bargain with %s") % (band.name,
                                                                                  gigbargain.venue.name)
                        )

    elif gigbargain_band.state == 'refused':
        messages.warning(request, _("You (%s) have already refused this bargain") % (band.name))
    
    return redirect(gigbargain)


def gigbargain_band_quit(request, band_slug, gigbargain_uuid):

    """
    A band can quit a bargain at any time
    """
    pass


def gigbargain_band_part_display(request, band_slug, gigbargain_uuid):
    """
    Display the part of a bargain concerning the given band
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('band_nego', 'band_ok', 'concluded') \
            or gigbargainband.state not in ('negociating', 'part_validated'):
            # XXX: Maybe it should more explicit
            return HttpResponseForbidden()

    # See if we have to ask for more informations
    data = model_to_dict(gigbargainband)
    data['set_duration'] = from_timedelta(timedelta(microseconds=data['set_duration'])) # XXX Little hack to work around durationfield bug
    gigbargainband_form = GigBargainBandPartEditForm(data,
                                                     instance=gigbargainband)
    gigbargainband_is_valid = gigbargainband_form.is_valid()
    print "IS VALID", gigbargainband_is_valid, gigbargainband_form.errors

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband': gigbargainband,
                     'gigbargainband_is_valid': gigbargainband_is_valid}

    return render_to_response(template_name='event/gigbargain_band_part.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )


def gigbargain_band_part_approve(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band accept its band part
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargainband.state != 'negociating':
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    # See if it can be approved with these information or if we need more
    # Redirect to form edit if can't be approved in state
    data = model_to_dict(gigbargainband)
    data['set_duration'] = from_timedelta(timedelta(microseconds=data['set_duration'])) # XXX Little hack to work around durationfield bug
    gigbargainband_form = GigBargainBandPartEditForm(data,
                                                     instance=gigbargainband)
    if not gigbargainband_form.is_valid():
        return redirect('event:gigbargain-band-part-edit', 
                        gigbargain_uuid=gigbargain.pk, 
                        band_slug=gigbargainband.band.slug)

    gigbargainband.approve_part()

    return redirect(gigbargain)


def gigbargain_band_part_edit(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band edit its band part
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('band_nego', 'band_ok'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband_form = GigBargainBandPartEditForm(request.POST or None, instance=gigbargainband)

    if request.method == 'POST':
        if gigbargainband_form.is_valid():
            # Save and approve our part
            gigbargainband = gigbargainband_form.save()
            gigbargainband.approve_part()

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband': gigbargainband,
                     'gigbargainband_form': gigbargainband_form}

    return render_to_response(template_name='event/gigbargain_band_part_edit.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )


from event.forms import GigBargainForBandForm

def gigbargain_band_common_edit(request, gigbargain_uuid, band_slug):
    """
    For a Band, edit the common conditions of the bargain.
    If changed, it reset all other bargainers' state.
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

    if gigbargain.state not in ('band_nego', 'band_ok'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargain_form = GigBargainForBandForm(request.POST or None,
                                            instance=gigbargain)

    if request.method == 'POST':
        if gigbargain_form.is_valid():
            gigbargain = gigbargain_form.save()

            # We have to invalide every part that have approbed
            for gigbargainband in gigbargain.gigbargainband_set.all():
                if gigbargainband.state == 'part_validated':
                    gigbargainband.cancel_approval()

            # Cancel the agreement if the gig bargain was approved by every band
            gigbargain.bands_dont_agree_anymore()


            gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)
            return redirect('event:gigbargain-band-part-edit', gigbargain.pk, band_slug)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargain_form': gigbargain_form}        

    return render_to_response(template_name='event/gigbargain_common_edit.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )
