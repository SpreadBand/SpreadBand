from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from elsewhere.forms import SocialNetworkForm, WebsiteForm

from ..models import Band

@login_required
def socialnet_associate_callback(request, band_slug, access, token):
    """
    Callback that associates a band with a social network account
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden(_("You are not allowed to manage this band"))

    # Save the association into database
    access.persist(band, token)

    messages.success(request,
                     _("%(band_name)s was successfully associated with %(service_name)s" % {"band_name": band.name,
                                                                                            "service_name": access.service}
                       )
                     )

    if hasattr(request, "session"):
        redirect_to = request.session.get('redirect_to', None)
        if redirect_to:
            return redirect(redirect_to)

    return render_to_response(template_name="blank_auto_closing_page.html")

    # return redirect(band)

from socialbridge.views import post_message, broadcast_message
from socialbridge.forms import SocialMessageForm

@login_required
def socialnet_post_message(request, band_slug, service):
    """
    Post a message on a social network
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden(_("You are not allowed to post a message for this band"))

    return post_message(request, band, service)

@login_required
def socialnet_broadcast_message(request, band_slug):
    """
    Post a message on a social network
    """
    band = get_object_or_404(Band, slug=band_slug)

    # Permissions
    if not request.user.has_perm('band.can_manage', band):
        return HttpResponseForbidden(_("You are not allowed to post a message for this band"))

    return broadcast_message(request, band)


@login_required
def socialnet_add(request, band_slug):
    pass

@login_required
def socialnet_edit(request, band_slug):
    band = get_object_or_404(Band, slug=band_slug)

    if request.method == 'POST':
        new_data = request.POST.copy()

        # Add forms
        if new_data.get('sn-form') or new_data.get('w-form'):
            if new_data.get('sn-form'):
                form = SocialNetworkForm(new_data)

            elif new_data.get('w-form'):
                form = WebsiteForm(new_data)

            if form.is_valid():
                profile = form.save(commit=False)
                profile.object = band
                profile.save()

                return HttpResponseRedirect(request.path)

        # Delete forms
        elif new_data.get('delete-sn-form') or new_data.get('delete-w-form'):
            delete_id = request.POST['delete_id']

            if new_data.get('delete-sn-form'):
                band.socialnetworks.get(id=delete_id).delete()

            elif new_data.get('delete-w-form'):
                band.websites.get(id=delete_id).delete()

            return HttpResponseRedirect(request.path)

        # WTF?
        else:
            return HttpResponseServerError

    # Create blank forms
    sn_form = SocialNetworkForm()
    w_form = WebsiteForm()

    return render_to_response(template_name='band/socialnets_edit.html', 
                              dictionary={'band': band,
                                          'sn_form': sn_form,
                                          'w_form': w_form,
                                          },
                              context_instance=RequestContext(request))



