from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm

def home_spreadband(request):
    """
    If not logged, show home page
    else, show user's page
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('account:detail', args=[request.user.username]))
    else:
        auth_form = AuthenticationForm()

        return render_to_response('home.html',
                                  dictionary={'auth_form': auth_form}
                                  )
                              




