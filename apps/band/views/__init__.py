from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail

from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from authority.decorators import permission_required_or_403

from django.contrib.auth.decorators import login_required

from ..models import Band
from ..forms import BandCreateForm, BandUpdateForm, BandMemberRequestForm


#@permission_required_or_403('band_permission.add_band')
@login_required
def new_or_own(request, band_slug=None):
    """
    register a new band or own an existing one
    """
    # We are owning an existing band
    if band_slug:
        band = get_object_or_404(Band, slug=band_slug)
        if band.owned:
            return render_to_response(request,
                                      template_name='band/band_already_owned.html'
                                      )
        else:
            if request.method == 'POST':
                bandform = BandCreateForm(request.POST, instance=band)
                if bandform.is_valid():
                    band = bandform.save(commit=False)
                    # mark the band as owned
                    band.owned = True
                    band.save()

                    return redirect(band)
            else:
                bandform = BandCreateForm(instance=band)

            return render_to_response(template_name='bands/band_new.html',
                                      dictionary={'band': band,
                                                  'form': bandform},
                                      context_instance=RequestContext(request),
                                      )

    # We are creating a new one
    else:
        return create_object(request,
                             form_class=BandCreateForm,
                             template_name='bands/band_new.html',
                             )

def edit(request, band_slug):
    """
    edit a band
    """
    band = get_object_or_404(Band, slug=band_slug)
    return update_object(request,
                         form_class=BandUpdateForm,
                         slug=band_slug,
                         template_name='bands/band_update.html',
                         extra_context={'band': band},
                         )

                          
def list(request):
    """
    list all bands
    """
    return object_list(request,
                       queryset=Band.objects.all(),
                       template_name='bands/band_list.html',
                       template_object_name='band',
                       )

#-- events
def event_detail(request, band_slug):
    pass

def event_new(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    return create_object(request,
                         form_class=GigForm,
                         template_name='bands/event_new.html',
                         extra_context={'band': band}
                         )
    


from bargain.models import Party, ContractParty, Contract
from django.contrib.contenttypes.models import ContentType

def detail(request, band_slug):
    """
    Show details about a band
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Get the bargains we're involved into
    band_type = ContentType.objects.get_for_model(band)
    try:
        party = Party.objects.get(content_type__pk=band_type.id,
                                  object_id=band.id)
        contracts = Contract.objects.filter(parties__contractparty__party=party)
    except Party.DoesNotExist:
        contracts = []

    return object_detail(request,
                         queryset=Band.objects.all(),
                         slug=band_slug,
                         template_object_name='band',
                         template_name='bands/band_detail.html',
                         extra_context={'contracts' : contracts},
                         )


    

#--- PICTURES
from ..forms import BandPictureForm

def picture_new(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    if request.method == 'POST':
        picture_form = BandPictureForm(request.POST, request.FILES)

        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.band = band

            picture.save()

            return redirect(band)

    return create_object(request,
                         form_class=BandPictureForm,
                         template_name='bands/picture_new.html',
                         extra_context={'band': band}
                         )
