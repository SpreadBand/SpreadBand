from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic.create_update import update_object

from notification.models import Notice

from profiles.views import edit_profile, profile_detail

from actstream.models import Action
from band.models import Band
from gigbargain.models import GigBargain

from .models import UserAvatar

from .forms import UserProfileForm, UserForm, AccountEditForm
from .forms import ProfileEditForm, ProfileAvatarForm

@login_required
def edit(request, username):
    return edit_profile(request,
                        form_class=ProfileEditForm,
                        success_url='#')

@login_required
def password(request):
    return update_object(request,
                         form_class=AccountEditForm,
                         object_id=request.user.id,
                         template_name='account/password.html',
                         post_save_redirect="?",
                         extra_context={'profile': request.user.get_profile()})

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
    if request.user.username == username:
        return dashboard(request)
    else:
        user = get_object_or_404(User, username=username)
        today = date.today()
        month_gigbargains = GigBargain.objects.filter(bands__in=user.bands.all, date__year=today.year, date__month=today.month).order_by('date')
        band_connections = Band.objects.filter(gigbargains__in=month_gigbargains).exclude(pk__in=user.bands.all).distinct()
        user_connections = User.objects.filter(bands__in=band_connections).distinct()[:20]
        return profile_detail(request, username,
                              extra_context={'user_connections': user_connections}
                              )

@login_required
def dashboard(request):
    notices = Notice.objects.notices_for(request.user, on_site=True)[:10]

    # Get all connections with other users this month
    today = date.today()
    month_gigbargains = GigBargain.objects.filter(bands__in=request.user.bands.all, date__year=today.year, date__month=today.month).order_by('date')
    band_connections = Band.objects.filter(gigbargains__in=month_gigbargains).exclude(pk__in=request.user.bands.all).distinct()
    user_connections = User.objects.filter(bands__in=band_connections).distinct()[:20]

    # Latest activity in bargains
    my_bands_gigbargains = GigBargain.objects.inprogress_gigbargains().filter(bands__in=request.user.bands.all)
    latest_activity = Action.objects.stream_for_model(GigBargain).filter(target_object_id__in=my_bands_gigbargains)[:10]

    context = {'notices': notices,
               'user_connections': user_connections,
               'latest_activity': latest_activity}

    return render_to_response(template_name='account/user_dashboard.html',
                              context_instance=RequestContext(request,
                                                              context)
                              )

@login_required
def contacts(request):
    context = {}
    return render_to_response(template_name='account/contacts.html',
                              context_instance=RequestContext(request,
                                                              context)
                              )
