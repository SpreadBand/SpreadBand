import datetime

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

from event.forms import GigBargainNewFromVenueForm, GigBargainBandForm, BaseGigBargainBandFormSet
from event.models import GigBargain

@login_required
@require_http_methods(["GET", "POST"])
def gigbargain_new_from_venue(request):
    """
    Initiate a gig bargain from a venue point of view
    """
    # Create the formset for bands
    GigBargainBandFormSet = formset_factory(GigBargainBandForm,
                                            formset=BaseGigBargainBandFormSet,
                                            extra=1,
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

                # Warn bands that they've got a new bargain proposal
                # XXX: This is suboptimal I guess
                users = []
                for band in gigbargain.bands.all():
                    for member in band.members.all():
                        users.append(member.user)
                
                notification.send(users,
                                  'gigbargain_proposal',
                                  {'gigbargain': gigbargain}
                                  )

                return redirect(gigbargain)

    context = {'gigbargain_form': gigbargain_form,
               'gigbargain_bands_formset': gigbargain_bands_formset}

    return render_to_response(template_name='event/gigbargain_new_from_venue.html',
                              context_instance=RequestContext(request,
                                                              context)
                              )



def gigbargain_venue_confirm_bands(request, gigbargain_uuid):
    """
    Let the venue confirm it wants to go on with the bands that have
    accepted.
    This case is triggered only when /some/ of the bands have accepted
    to bargain, not all.
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

    if gigbargain.state != 'need_venue_confirm':
        # XXX Maybe we should be more explicit
        return HttpResponseForbidden()

    gigbargain.start_band_negociation()

    return redirect(gigbargain)

def gigbargain_venue_conclude(request, gigbargain_uuid):
    """
    Once all bands have agreed, conclude the bargain
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

    if gigbargain.state != 'band_ok':
        # XXX Maybe we should be more explicit
        return HttpResponseForbidden()
    
    gigbargain.conclude()

    return redirect(gigbargain)

from event.forms import GigBargainForVenueForm

def gigbargain_venue_common_edit(request, gigbargain_uuid):
    """
    For a Venue, edit the common conditions of the bargain.
    If changed, it reset all bands' state.
    """
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_uuid)

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

    return render_to_response(template_name='event/gigbargain_common_edit.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )
