"""
Membership management for a band
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic.create_update import delete_object, create_object
from django.views.generic.list_detail import object_list

from guardian.shortcuts import assign

from ..forms import BandMemberRequestForm, BandMemberAddForm
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


@login_required
def membership_add(request, band_slug):
    """
    Add a member in the band
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden(_("You are not allowed to edit this band"))

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
            assign('band.can_manage', request.user, band)

            return redirect(bandmember)

    return create_object(request,
                         form_class=BandMemberAddForm,
                         template_name='band/membership_add.html',
                         extra_context={'band': band},
                         )

@login_required
def membership_manage(request, band_slug):
    """
    Manage members in the band
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden('You are not allowed to edit this band')

    return object_list(request,
                       queryset=BandMember.objects.filter(band__id=band.id),
                       template_name='band/membership_manage.html',
                       template_object_name='bandmember',
                       extra_context={'band': band}
                       )


@login_required
def membership_remove(request, band_slug, member_id):
    """
    Remove a member from the band
    """
    band = get_object_or_404(Band, slug=band_slug)
    bandmember = get_object_or_404(BandMember, band=band.id, user=member_id)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden(_("You are not allowed to edit this band"))

    if len(band.members.all()) == 1:
        messages.error(request, _("You can't let this band alone"))
        return redirect('band:membership-manage', band.slug)

    return delete_object(request,
                         model=BandMember,
                         object_id=bandmember.id,
                         template_name='band/bandmember_confirm_delete.html',
                         template_object_name='bandmember',
                         post_delete_redirect=bandmember.get_absolute_url(),
                         extra_context={'band': band}
                         )
    
