from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from .models import UserProfile, UserAvatar

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserAvatar
        fields = ('original_image',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'birthdate', 'email', 'country', 'timezone', 'town')

    email = forms.EmailField(label=_("Email address"),
                             help_text='')

    first_name = forms.CharField(label=_("First name"), 
                                 max_length=30,
                                 required=False)

    last_name = forms.CharField(label=_("Last name"), 
                                max_length=30,
                                required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
     
    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileEditForm, self).save(*args,**kwargs)
        return profile

