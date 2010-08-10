import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

import notification.models as notification

from apps.band.models import Band
from apps.venue.models import Venue

import gigbargain.signals as signals
from ..forms import GigBargainNewFromVenueForm, GigBargainBandForm, BaseGigBargainBandFormSet, GigBargainForVenueForm
from ..forms import GigBargainBandInviteForm, VenueReasonForm
from ..models import GigBargain

@login_required
@require_http_methods(["GET", "POST"])
def gigbargain_new_from_venue(request):
    """
    Initiate a gig bargain from a venue point of view
    """
    # Create the formset for bands
    GigBargainBandFormSet = formset_factory(GigBargainBandForm,
                                            formset=BaseGigBargainBandFormSet,
                                            extra=1, # XXX Maybe I should increment this to prevent forms to be zeored
                                            )

    initial_form_data = {}

    if request.method == 'GET':
        # Set the venue if specified
        if request.GET.has_key('venue'):
            venue = get_object_or_404(Venue, slug=request.GET['venue'])
            initial_form_data['venue'] = venue.id

        # Set the date if specified
        if request.GET.has_key('date'):
            initial_form_data['date'] = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d')

        gigbargain_form = GigBargainNewFromVenueForm(aUser=request.user, 
                                                     initial=initial_form_data,
                                                     )

        gigbargain_bands_formset = GigBargainBandFormSet()

    elif request.method == 'POST':
        # If requested to add a band
        if 'add_band' in request.POST:
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
            request.POST = cp

        gigbargain_form = GigBargainNewFromVenueForm(request.user,
                                                     request.POST)

        gigbargain_bands_formset = GigBargainBandFormSet(request.POST)

        if 'submit' in request.POST:
            # Save bargain+bands if valid
            if gigbargain_form.is_valid() and gigbargain_bands_formset.is_valid():            
                gigbargain = gigbargain_form.save(commit=False)
                gigbargain.save()
            
                formset = GigBargainBandFormSet(request.POST)
        
                # Assign this gig bargain for each band
                if formset.is_valid():
                    for form in formset.forms:
                        bargainband = form.save(commit=False)
                        # XXX: had to do that to prevent from saving empty forms
                        if bargainband.band_id:
                            bargainband.bargain = gigbargain
                            bargainband.save()


                signals.gigbargain_new_from_venue.send(sender=gigbargain.venue,
                                                       aGigBargain=gigbargain)

                # Warn bands that they've got a new bargain proposal
                # XXX: This is suboptimal I guess
                # users = []
                # for band in gigbargain.bands.all():
                #     for member in band.members.all():
                #         users.append(member.user)
                
                # notification.send(users,
                #                   'gigbargain_proposal',
                #                   {'gigbargain': gigbargain}
                #                   )

                return redirect(gigbargain)

    context = {'gigbargain_form': gigbargain_form,
               'gigbargain_bands_formset': gigbargain_bands_formset}

    return render_to_response(template_name='gigbargain/gigbargain_new_from_venue.html',
                              context_instance=RequestContext(request,
                                                              context)
                              )


@login_required
def gigbargain_venue_confirm_bands(request, gigbargain_uuid):
    """
    Let the venue confirm it wants to go on with the bands that have
    accepted.
    This case is triggered only when /some/ of the bands have accepted
    to bargain, not all.
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()

    if gigbargain.state != 'need_venue_confirm':
        # XXX Maybe we should be more explicit
        return HttpResponseForbidden()

    gigbargain.start_band_negociation()

    return redirect(gigbargain)


@login_required
def gigbargain_venue_decline(request, gigbargain_uuid):
    """
    Decline a bargain
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()
    
    if gigbargain.state not in ('band_ok', 'complete_proposed_to_venue', 'incomplete_proposed_to_venue'):
        # XXX Maybe we should be more explicit
        return HttpResponseForbidden()


    reason_form = VenueReasonForm(request.POST or None)

    if request.method == 'POST' and reason_form.is_valid(): 
        gigbargain.venue_reason = reason_form.cleaned_data['venue_reason']
        gigbargain.decline()

        return redirect(gigbargain)
    else:
        extra_context = {'gigbargain': gigbargain,
                         'reason_form': reason_form}

        return render_to_response(template_name='gigbargain/gigbargain_venue_decline.html',
                                  context_instance=RequestContext(request,
                                                                  extra_context)
                                  )



@login_required
def gigbargain_venue_conclude(request, gigbargain_uuid):
    """
    Once all bands have agreed, conclude the bargain
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()

    if gigbargain.state not in ('band_ok', 'complete_proposed_to_venue'):
        # XXX Maybe we should be more explicit
        return HttpResponseForbidden()

    gigbargain.conclude()

    return redirect(gigbargain)


@login_required
def gigbargain_venue_cancel(request, gigbargain_uuid):
    """
    Cancel a bargain, even if bands are ok
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()

    if gigbargain.state not in ('need_venue_confirm'):
        # XXX Maybe we should be more explicit
        return HttpResponseForbidden()

    gigbargain.cancel()

    return redirect(gigbargain)


@login_required
def gigbargain_venue_enter_negociations(request, gigbargain_uuid):
    """
    When a gigbargain is proposed by bands to a venue, a venue can
    choose to enter the negociations.
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()

    if gigbargain.state not in ('complete_proposed_to_venue', 'incomplete_proposed_to_venue'):
        # XXX Maybe we should be more explicit
        return HttpResponseForbidden()
    
   
    # XXX not sure we want to keep this
    # if this is an incomplete bargain, just make the bands enter
    # negociations
    if gigbargain.state == 'incomplete_proposed_to_venue':
        [gigbargainband.start_negociating()
         for gigbargainband 
         in gigbargain.gigbargainband_set.all()]
        
        
    # else, if it is a complete bargain, we have to invalidate the
    # bands approval
    elif gigbargain.state == 'complete_proposed_to_venue':
        [gigbargainband.cancel_approval()
         for gigbargainband
         in gigbargain.gigbargainband_set.filter(state='part_validated')]

        
    # Then, switch our gigbargain state by letting the venue enter
    gigbargain.venue_enter_negociations()

    return redirect(gigbargain)

@login_required
def gigbargain_venue_common_edit(request, gigbargain_uuid):
    """
    For a Venue, edit the common conditions of the bargain.
    If changed, it reset all bands' state.
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()

    if gigbargain.state not in ('new', 'need_venue_confirm', 'band_nego', 'band_ok'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargain_form = GigBargainForVenueForm(request.POST or None,
                                             instance=gigbargain)

    if request.method == 'POST':
        if gigbargain_form.is_valid():
            gigbargain = gigbargain_form.save()

            # If we were negociating, then invalidate required parts
            if gigbargain.state in ('band_nego', 'band_ok'):
                # We have to invalide every part that have approbed
                for gigbargainband in gigbargain.gigbargainband_set.all():
                    if gigbargainband.state == 'part_validated':
                        gigbargainband.cancel_approval()

                # Cancel the agreement if the gig bargain was approved by every band
                gigbargain.bands_dont_agree_anymore()

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargain_form': gigbargain_form}        

    return render_to_response(template_name='gigbargain/gigbargain_common_edit.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )



@login_required
def gigbargain_venue_renegociate(request, gigbargain_uuid):
    """
    When a bargain has been approved, restart negociations if something is incorrect
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()

    if gigbargain.state not in ('band_ok'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    reason_form = VenueReasonForm(request.POST or None)

    if request.method == 'POST' and reason_form.is_valid():
        for gigbargainband in gigbargain.gigbargainband_set.filter(state='part_validated'):
            gigbargainband.cancel_approval()

        # Save the reason and reset band states
        gigbargain.venue_reason = reason_form.cleaned_data['venue_reason']
        gigbargain.bands_dont_agree_anymore()

        return redirect(gigbargain)
    else:
        extra_context = {'gigbargain': gigbargain,
                         'reason_form': reason_form}

        return render_to_response(template_name='gigbargain/gigbargain_venue_renegociate.html',
                                  context_instance=RequestContext(request,
                                                                  extra_context)
                                  )
                                  

@login_required
def gigbargain_venue_invite_band(request, gigbargain_uuid):
    """
    When a Venue invites another Band to join a bargain
    """
    gigbargain = get_object_or_404(GigBargain, uuid=gigbargain_uuid)

    if not request.user.has_perm('venue.can_manage', gigbargain.venue):
        return HttpResponseForbidden()

    if gigbargain.state not in ('new', 'need_venue_confirm', 'band_nego'):
        # XXX: Maybe it should more explicit
        return HttpResponseForbidden()

    gigbargainband_form = GigBargainBandInviteForm(gigbargain,
                                                   request.POST or None)

    if request.method == 'POST':
        if gigbargainband_form.is_valid():
            gigbargainband = gigbargainband_form.save(commit=False)
            gigbargainband.bargain = gigbargain
            gigbargainband.save()

            messages.success(request, _("%s was successfully invited") % gigbargainband.band.name)

            # If there were bands that had validated their part, invalidate them
            for gigbargainband in gigbargain.gigbargainband_set.filter(state='part_validated'):
                gigbargainband.cancel_approval()

            return redirect(gigbargain)

    extra_context = {'gigbargain': gigbargain,
                     'gigbargainband_form': gigbargainband_form}

    return render_to_response(template_name='gigbargain/gigbargain_invite_band.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )
