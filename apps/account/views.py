from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render_to_response

from django.http import HttpResponse
from django.template.context import RequestContext

from notification.models import Notice

from profiles.views import edit_profile, profile_detail

from .forms import UserProfileForm, UserForm
from .forms import ProfileEditForm

@login_required
def edit(request, username):
    return edit_profile(request,
                        form_class=ProfileEditForm,
                        success_url='#')

@login_required
def detail(request, username):
    return profile_detail(request, username)

@login_required
def dashboard(request):
    notices = Notice.objects.notices_for(request.user, on_site=True)

    context = {'notices': notices}

    return render_to_response(template_name='account/user_dashboard.html',
                              context_instance=RequestContext(request,
                                                              context)
                              )

