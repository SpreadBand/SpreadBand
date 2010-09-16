from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

# from durationfield.utils.timestring import from_timedelta
import notification.models as notification
from actstream.models import action

from apps.band.models import Band
from apps.venue.models import Venue

from ..models import GigBargain, GigBargainBand
from ..forms import GigBargainBandPartEditForm, GigBargainNewFromBandForm, GigBargainMyBandForm
from ..forms import GigBargainBandInviteForm, GigBargainForBandForm, GigBargainBandRefuseForm
from ..forms import GigBargainBandTimelineForm, GigBargainBandRemunerationForm, GigBargainBandDefraymentForm

@login_required
def gigbargain_new_from_band(request, band_slug):
    """
    For a Band, create a new gigbargain
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain_form = GigBargainNewFromBandForm(request.user,
                                                request.POST or None)
    gigbargain_myband_form = GigBargainMyBandForm(request.POST or None)

    if request.method == 'POST':
        if gigbargain_form.is_valid() and gigbargain_myband_form.is_valid():
            gigbargain = gigbargain_form.save()

            # Set bargain and band to what is supposed to be our band form, then save
            gigbargain_myband = gigbargain_myband_form.save(commit=False)
            gigbargain_myband.bargain = gigbargain
            gigbargain_myband.band = band

            gigbargain_myband.state = 'negociating'
            gigbargain_myband.save()

            # Make it a draft
            gigbargain.become_draft()

            return redirect(gigbargain)

    extra_context = {'band': band,
                     'gigbargain_form': gigbargain_form,
                     'gigbargain_myband_form': gigbargain_myband_form}

    return render_to_response(template_name='gigbargain/gigbargain_new_from_band.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )

@login_required
def gigbargain_enter_for_band(request, band_slug, gigbargain_uuid):
    """
    Enter a bargain, for a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    gigbargain_band = get_object_or_404(GigBargainBand, 
                                        bargain__uuid=gigbargain_uuid,
                                        band__slug=band_slug)
    
    if gigbargain.state not in ('new', 'draft', 'band_nego'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    # If we were waiting, switch to "accepted" and save
    if gigbargain_band.state == 'waiting':
        gigbargain_band.accept()

        # Negociations haven't already started
        if gigbargain.state == 'new':
            # If everybody has accepted, bands can start negociating
            if all([gigbargain_band.state == 'accepted' for gigbargain_band in gigbargain.gigbargainband_set.all()]):
                for gigbargain_band in gigbargain.gigbargainband_set.all():
                    gigbargain_band.start_negociating()

                # Then, update bargain state
                gigbargain.start_band_negociation()

        
            # If /SOME/ of the bands have accepted, ask the venue if we start negociation or not
            elif all([gigbargain_band.state != 'waiting' for gigbargain_band in gigbargain.gigbargainband_set.all()]):
                gigbargain.need_venue_confirmation()

        # If negociations have already started
        elif gigbargain.state in ('draft', 'band_nego'):
            gigbargain_band.start_negociating()

            # Since we're joining, invalidate all parts of other bands
            for gigbargainband in gigbargain.gigbargainband_set.all():
                if gigbargainband.state == 'part_validated':
                    gigbargainband.cancel_approval()

        # Send the action
        action.send(gigbargain_band, verb='gigbargain_entered', target=gigbargain, public=False)

        messages.success(request, _("You (%(band_name)s) are now bargaining with %(venue_name)s") % {'band_name': band.name,
                                                                                                     'venue_name': gigbargain.venue.name}
                         )



    # If not, warn we have already entered the bargain
    elif gigbargain_band.state in ('accepted', 'negociating', 'validated'):
        messages.warning(request, _("You (%(band_name)s) are already bargaining with %(venue_name)s") % {'band_name': band.name,
                                                                                                         'venue_name': gigbargain.venue.name}
                         )

    # If we're no more in the bargain
    elif gigbargain_band.state in ('refused', 'exited', 'kicked'):
        messages.error(request, _("You are no more part of this bargain"))

    return redirect(gigbargain)


# XXX: beware of state : should be more constrained
@login_required
def gigbargain_refuse_for_band(request, band_slug, gigbargain_uuid):
    """
    For a Band, don't enter a gigbargain and so refuse it.
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargain_band = get_object_or_404(GigBargainBand, 
                                        bargain__uuid=gigbargain_uuid,
                                        band__slug=band_slug)

    if gigbargain.state not in ('new', 'draft', 'band_nego'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    # Build the form
    refuse_form = GigBargainBandRefuseForm(request.POST or None)

    if request.method == 'POST' and refuse_form.is_valid():
        # If we were waiting, switch to "refused" and save
        if gigbargain_band.state == 'waiting':
            # Save the reason and refuse
            gigbargain_band.reason = refuse_form.cleaned_data['reason']
            gigbargain_band.refuse()

            action.send(gigbargain_band, verb='refused', target=gigbargain, public=False)

            messages.success(request, _("You (%(band_name)s) have refused to bargain with %(venue_name)s") % {'band_name': band.name,
                                                                                                              'venue_name': gigbargain.venue.name}
                             )

            if gigbargain.state == 'new':
                # If no more bands are waiting, trigger bargain state update
                if all([gigbargain_band.state != 'waiting' for gigbargain_band in gigbargain.gigbargainband_set.all()]):
                    gigbargain.need_venue_confirmation()

            elif gigbargain.state == 'draft':
                # Check if now, there are only bands with their parts
                # validated, because if so, validate the whole bargain
                gigbargainbands = gigbargain.gigbargainband_set.all()
                for state in 'waiting', 'accepted', 'negociating', 'exited', 'kicked', 'refused':
                    gigbargainbands = gigbargainbands.exclude(state=state)

                if len(gigbargainbands) and all([gigbargain_band.state == 'part_validated' for gigbargain_band in gigbargainbands]):
                    gigbargain.bands_have_approved_draft()

        elif gigbargain_band.state == 'refused':
            messages.warning(request, _("You (%s) have already refused this bargain") % (band.name))

        return redirect(gigbargain)

    else:
        extra_context = {'gigbargain': gigbargain,
                         'band': band,
                         'refuse_form': refuse_form}

        return render_to_response(template_name='gigbargain/gigbargain_band_refuse.html',
                                  context_instance=RequestContext(request,
                                                                  extra_context)
                                  )
    



@login_required
def gigbargain_band_quit(request, band_slug, gigbargain_uuid):

    """
    A band can quit a bargain at any time
    """
    pass


@login_required
def gigbargain_band_part_display(request, band_slug, gigbargain_uuid):
    """
    Display the part of a bargain concerning the given band
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('draft', 'draft_ok', 'band_nego', 'band_ok', 'concluded') \
            or gigbargainband.state not in ('negociating', 'part_validated'):
            # XXX: Maybe it should more explicit
            return HttpResponseForbidden()

    # See if we have to ask for more informations
    data = model_to_dict(gigbargainband)
    # data['set_duration'] = from_timedelta(timedelta(microseconds=data['set_duration'])) # XXX Little hack to work around durationfield bug
    print data['set_duration']
    gigbargainband_form = GigBargainBandPartEditForm(data,
                                                     instance=gigbargainband)
    gigbargainband_is_valid = gigbargainband_form.is_valid()

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband': gigbargainband,
                     'gigbargainband_is_valid': gigbargainband_is_valid}

    return render_to_response(template_name='gigbargain/gigbargain_band_part.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )


@login_required
def gigbargain_band_part_unlock(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band unlock its part
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargain_band = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('band_nego', 'draft') \
            or gigbargain_band.state != 'part_validated':
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    # if all bands agreed, then come back to "negociating" phase
    # if gigbargain.state == 'band_ok':
    #    gigbargain.bands_dont_agree_anymore()

    # Cancel approval for this band
    gigbargain_band.cancel_approval()

    action.send(gigbargain_band, verb='part_unlocked', target=gigbargain, public=False)

    messages.success(request, _("You have unlocked your part"))

    return redirect(gigbargain)


@login_required
def gigbargain_band_part_lock(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band accepts and locks its part
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargain_band = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('draft', 'band_nego') \
            or gigbargain_band.state not in ('negociating', 'part_validated'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    # See if it can be approved with these information or if we need more
    # Redirect to form edit if can't be approved in state
    data = model_to_dict(gigbargain_band)
    # XXX FIXME
    # data['set_duration'] = from_timedelta(timedelta(microseconds=data['set_duration'])) # XXX Little hack to work around durationfield bug
    gigbargainband_form = GigBargainBandPartEditForm(data,
                                                     instance=gigbargain_band)
    if not gigbargainband_form.is_valid():
        return redirect('gigbargain:gigbargain-band-part-edit', 
                        gigbargain_uuid=gigbargain.uuid, 
                        band_slug=gigbargain_band.band.slug)

    action.send(gigbargain_band, verb='part_locked', target=gigbargain, public=False)

    gigbargain_band.approve_part()
    messages.success(request, _("You have locked your part"))

    # If all bands have accepted their parts, then either :
    #  - set as band_ok if we were in band_nego
    #  - set as draft_ok if we were in draft
    if len(GigBargainBand.objects.filter(bargain=gigbargain, 
                                         state='negociating').exclude(id=gigbargain_band.id)) == 0:
        if gigbargain.state == 'band_nego':
            gigbargain.bands_have_approved_parts()
        elif gigbargain.state == 'draft':
            # We have to check that no band is still being invited.
            # If this is it the case, we don't validate the bargain
            if len(gigbargain.gigbargainband_set.filter(state='waiting')) == 0:
                gigbargain.bands_have_approved_draft()

    return redirect(gigbargain)


@login_required
def gigbargain_band_part_edit(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band edit its band part
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('draft', 'band_nego') \
            or  gigbargainband.state not in ('negociating'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband_form = GigBargainBandPartEditForm(request.POST or None, instance=gigbargainband)

    if request.method == 'POST':
        if gigbargainband_form.is_valid():
            # Save
            gigbargainband = gigbargainband_form.save()

            messages.success(request, _("Changes saved"))

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband': gigbargainband,
                     'gigbargainband_form': gigbargainband_form}

    return render_to_response(template_name='gigbargain/gigbargain_band_part_edit.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )


@login_required
def gigbargain_band_edit_timeline(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band edit its band part
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('draft', 'band_nego') \
            or  gigbargainband.state not in ('negociating'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband_form = GigBargainBandTimelineForm(request.POST or None, instance=gigbargainband)

    if request.method == 'POST':
        if gigbargainband_form.is_valid():
            # Save
            gigbargainband = gigbargainband_form.save()

            messages.success(request, _("Changes saved"))

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband': gigbargainband,
                     'gigbargainband_form': gigbargainband_form}

    return render_to_response(template_name='gigbargain/gigbargain_band_edit_timeline.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )


@login_required
def gigbargain_band_edit_remuneration(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band edit its band part
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('draft', 'band_nego') \
            or  gigbargainband.state not in ('negociating'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband_form = GigBargainBandRemunerationForm(request.POST or None, instance=gigbargainband)

    if request.method == 'POST':
        if gigbargainband_form.is_valid():
            # Save
            gigbargainband = gigbargainband_form.save()

            messages.success(request, _("Changes saved"))

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband': gigbargainband,
                     'gigbargainband_form': gigbargainband_form}

    return render_to_response(template_name='gigbargain/gigbargain_band_edit_remuneration.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )

@login_required
def gigbargain_band_edit_defrayment(request, band_slug, gigbargain_uuid):
    """
    During the band negociation phase, when a band edit its band part
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)
    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('draft', 'band_nego') \
            or  gigbargainband.state not in ('negociating'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband_form = GigBargainBandDefraymentForm(request.POST or None, instance=gigbargainband)

    if request.method == 'POST':
        if gigbargainband_form.is_valid():
            # Save
            gigbargainband = gigbargainband_form.save()

            messages.success(request, _("Changes saved"))

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband': gigbargainband,
                     'gigbargainband_form': gigbargainband_form}

    return render_to_response(template_name='gigbargain/gigbargain_band_edit_defrayment.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )




@login_required
def gigbargain_band_common_edit(request, gigbargain_uuid, band_slug):
    """
    For a Band, edit the common conditions of the bargain.
    If changed, it reset all other bargainers' state.
    """
    band = get_object_or_404(Band, slug=band_slug)

    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden()

    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if gigbargain.state not in ('draft', 'band_nego', 'band_ok'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargain_form = GigBargainForBandForm(request.POST or None,
                                            instance=gigbargain)

    if request.method == 'POST':
        if gigbargain_form.is_valid():
            gigbargain = gigbargain_form.save()

            # We have to invalidate every part that have been approved
            for gigbargainband in gigbargain.gigbargainband_set.all():
                if gigbargainband.state == 'part_validated':
                    gigbargainband.cancel_approval()

            # Cancel the agreement if the gig bargain was approved by every band
            if gigbargain.state == 'band_ok':
                gigbargain.bands_dont_agree_anymore()

            messages.success(request, _("You have successfully edited the general parts"))
            messages.warning(request, _("Remember, you need to lock your part again"))

            return redirect('gigbargain:gigbargain-detail', gigbargain.uuid)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargain_form': gigbargain_form,
                     'band': band}

    return render_to_response(template_name='gigbargain/gigbargain_common_edit.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )

# XXX Security
@login_required
def gigbargain_band_submit_draft_to_venue(request, gigbargain_uuid):
    """
    Submits a draft to the targetted venue
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if gigbargain.state != 'draft_ok':
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargain.propose_complete_bargain_to_venue()

    action.send(request.user, verb='submitted_to_venue', target=gigbargain, public=False)

    messages.success(request, _("The bargain was submitted to %s") % gigbargain.venue.name)

    return redirect(gigbargain)

# XXX Security
@login_required
def gigbargain_band_invite_band(request, gigbargain_uuid):
    """
    When a Band invites another Band to join a bargain
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if gigbargain.state not in ('draft'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband_form = GigBargainBandInviteForm(gigbargain,
                                                   request.POST or None)

    if request.method == 'POST':
        if gigbargainband_form.is_valid():
            gigbargainband = gigbargainband_form.save(commit=False)
            gigbargainband.bargain = gigbargain
            gigbargainband.save()

            # If there were bands that had validated their part, invalidate them
            for gigbargainband in gigbargain.gigbargainband_set.filter(state='part_validated'):
                gigbargainband.cancel_approval()

            action.send(gigbargainband, verb='was_invited', target=gigbargain, public=False)

            messages.success(request, _("%s was successfully invited") % gigbargainband.band.name)

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband_form': gigbargainband_form}

    return render_to_response(template_name='gigbargain/gigbargain_invite_band.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )
    
# XXX Security
@login_required
def gigbargain_band_draft_renegociate(request, gigbargain_uuid):
    """
    When a draft has been approved, restart negociations if something is incorrect
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if gigbargain.state not in ('draft_ok'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    for gigbargainband in gigbargain.gigbargainband_set.filter(state='part_validated'):
        gigbargainband.cancel_approval()

    gigbargain.bands_have_disapproved_draft()

    return redirect(gigbargain)


# XXX Security
@login_required
def gigbargain_band_kick(request, gigbargain_uuid, band_slug):
    """
    Kick the given band from the gig bargain
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    gigbargainband = get_object_or_404(GigBargainBand, bargain=gigbargain, band__slug=band_slug)

    if gigbargain.state not in ('draft'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband.kick()

    for gigbargainband in gigbargain.gigbargainband_set.filter(state='part_validated'):
        gigbargainband.cancel_approval()

    return redirect(gigbargain)
