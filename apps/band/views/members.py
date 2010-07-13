"""
Membership management for a band
"""
from django.views.generic.create_update import create_object
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_list

from ..forms import BandMemberRequestForm
from ..models import Band, BandMember

def membership_request(request, band_slug):
    """
    Request for being a member in this band
    """
    band = get_object_or_404(Band, slug=band_slug)

    if request.method == 'POST':
        membreq_form = BandMemberRequestForm(request.POST)

        if membreq_form.is_valid():
            membreq = membreq_form.save(commit=False)
            membreq.user = request.user
            membreq.band = band
            
            membreq.save()

            return redirect(band)
    
    return create_object(request,
                         form_class=BandMemberRequestForm,
                         template_name='bands/membership_request.html',
                         extra_context={'band': band},
                         )


from ..forms import BandMemberAddForm
from django.contrib.auth.models import User

from guardian.shortcuts import assign

def membership_add(request, band_slug):
    """
    Add a member in the band
    """
    band = get_object_or_404(Band, slug=band_slug)

    if request.method == 'POST':
        addform = BandMemberAddForm(request.POST)

        if addform.is_valid():
            # Set band
            bandmember = addform.save(commit=False)
            bandmember.band = band

            # Save to DB
            bandmember.save()
            addform.save_m2m()

            # Assign rights to the user
            assign('band.change_band', request.user, band)

            return redirect(bandmember)

    return create_object(request,
                         form_class=BandMemberAddForm,
                         template_name='band/membership_add.html',
                         extra_context={'band': band},
                         )

def membership_manage(request, band_slug):
    """
    Manage members in the band
    """
    band = get_object_or_404(Band, slug=band_slug)

    return object_list(request,
                       queryset=BandMember.objects.filter(band__id=band.id),
                       template_name='band/membership_manage.html',
                       template_object_name='bandmember',
                       extra_context={'band': band}
                       )


from django.views.generic.create_update import delete_object

def membership_remove(request, band_slug, member_id):
    """
    Remove a member from the band
    """
    band = get_object_or_404(Band, slug=band_slug)
    bandmember = get_object_or_404(BandMember, band=band.id, user=member_id)

    return delete_object(request,
                         model=BandMember,
                         object_id=bandmember.id,
                         template_name='band/bandmember_confirm_delete.html',
                         template_object_name='bandmember',
                         post_delete_redirect=bandmember.get_absolute_url(),
                         extra_context={'band': band}
                         )
    
