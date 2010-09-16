from django.shortcuts import get_object_or_404
from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

from .models import GigBargain, GigBargainBand
from .forms import GigBargainBandInviteForm, GigBargainBandTimelineForm
from .forms import GigBargainBandRemunerationForm, GigBargainBandDefraymentForm
from .forms import GigBargainForBandForm

def submit_form(request, form_id, form, gigbargainband):
    dajax = Dajax()

    if form.is_valid():
        dajax.remove_css_class('%s input' % form_id, 'error')
        dajax.script("$('%s').submit()" % form_id)
    else:
        dajax.remove_css_class('%s input' % form_id, 'error')
        for error in form.errors:
            dajax.add_css_class('#id_%s' % error, 'error')
            
    return dajax.json()

#-- Common
def access_edit(request, gigbargain_id, form):
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_id)
    form = GigBargainForBandForm(form)
    return submit_form(request, '#access-form', form, gigbargain)

#-- Band specific
def timeline_edit(request, gigbargainband_id, form):
    gigbargainband = get_object_or_404(GigBargainBand, pk=gigbargainband_id)
    form = GigBargainBandTimelineForm(form)
    return submit_form(request, '#timeline-form', form, gigbargainband)

def remuneration_edit(request, gigbargainband_id, form):
    gigbargainband = get_object_or_404(GigBargainBand, pk=gigbargainband_id)
    form = GigBargainBandRemunerationForm(form)
    return submit_form(request, '#remuneration-form', form, gigbargainband)    

def defrayment_edit(request, gigbargainband_id, form):
    gigbargainband = get_object_or_404(GigBargainBand, pk=gigbargainband_id)
    form = GigBargainBandDefraymentForm(form)
    return submit_form(request, '#defrayment-form', form, gigbargainband)    

def band_invite(request, gigbargain_id, form):
    gigbargain = get_object_or_404(GigBargain, pk=gigbargain_id)
    form = GigBargainBandInviteForm(gigbargain, form)
    return submit_form(request, '#band-invite-form', form, gigbargain)

        
dajaxice_functions.register(band_invite)
dajaxice_functions.register(timeline_edit)
dajaxice_functions.register(remuneration_edit)
dajaxice_functions.register(defrayment_edit)
dajaxice_functions.register(access_edit)






