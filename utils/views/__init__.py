from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse

from userena.forms import AuthenticationForm

from band.models import Band

def home_spreadband(request):
    """
    If not logged, show home page
    else, show user's page
    """
    user = request.user

    if user.is_authenticated and not user.is_anonymous():
        user_bands = user.bands.all()
        user_venues = user.venues.all()

        # If we only have ONE BAND and no venue
        if user_bands.count() == 1 and user_venues.count() == 0:
            return redirect(user_bands.all()[0])
        # If we only have ONE VENUE and no band
        elif user_venues.count() == 1 and user_bands.count() == 0:
            return redirect(user_venues.all()[0])
        # We manage multiple entities
        else:
            return HttpResponseRedirect(reverse('account:dashboard'))
    else:
        auth_form = AuthenticationForm()

        latest_bands = Band.objects.order_by('-registered_on')[:11]

        return render_to_response('home.html',
                                  dictionary={'auth_form': auth_form,
                                              'latest_bands': latest_bands},
                                  context_instance=RequestContext(request),
                                  )
                              




