from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm

def home_spreadband(request):
    """
    If not logged, show home page
    else, show user's page
    """
    if request.user.is_authenticated and not request.user.is_anonymous():
        # If we only have one band, then go to this page, else send to dashboard
        if request.user.bands.count() == 1:
            return redirect(request.user.bands.all()[0])
        else:
            return HttpResponseRedirect(reverse('account:detail', args=[request.user.username]))
    else:
        auth_form = AuthenticationForm()

        return render_to_response('home.html',
                                  dictionary={'auth_form': auth_form}
                                  )
                              




