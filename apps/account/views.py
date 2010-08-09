from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render_to_response, redirect

from django.http import HttpResponse
from django.template.context import RequestContext

from notification.models import Notice

from profiles.views import edit_profile, profile_detail

from .models import UserAvatar

from .forms import UserProfileForm, UserForm
from .forms import ProfileEditForm, ProfileAvatarForm

@login_required
def edit(request, username):
    return edit_profile(request,
                        form_class=ProfileEditForm,
                        success_url='#')

@login_required
def avatar_set(request):
    """
    Create or update an avatar for a user
    """
    profile = request.user.get_profile()

    if request.method == 'POST':
        avatar_form = ProfileAvatarForm(request.POST,
                                        request.FILES)

        if avatar_form.is_valid():
            # Edit
            try:
                avatar = profile.avatar
                avatar.original_image = avatar_form.cleaned_data['original_image']
                avatar.save()
            # Creation
            except UserAvatar.DoesNotExist:
                avatar_image = avatar_form.save(commit=False)
                avatar_image.userprofile = profile
                avatar_image.save()

            return redirect(profile)
    else:
        avatar_form = ProfileAvatarForm()

    extra_context = {'avatar_form': avatar_form}
        
    return render_to_response(template_name='account/profile_avatar.html',
                              context_instance=RequestContext(request,
                                                              extra_context)
                              )

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

