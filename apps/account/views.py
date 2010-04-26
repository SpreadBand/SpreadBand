from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render_to_response

from django.http import HttpResponse
from django.template.context import RequestContext

from .forms import UserProfileForm, UserForm

@login_required
def detail(request):
    """
    Show details of a profile
    """
    user = request.user
    profile = user.get_profile()

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render_to_response(template_name='account/account_detail.html',
                              dictionary={'profile_form': profile_form,
                                          'user_form' : user_form},
                              context_instance=RequestContext(request),
                              )
