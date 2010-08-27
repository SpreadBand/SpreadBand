from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from elsewhere.forms import SocialNetworkForm, WebsiteForm

from ..models import Band

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



