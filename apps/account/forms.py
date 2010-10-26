import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile, UserAvatar

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'genre']


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserAvatar
        fields = ('original_image',)


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']

    password1 = forms.CharField(label=_("New password"),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("Confirm password"),
                                widget=forms.PasswordInput())
        

    def clean(self):
        """
        If the user wants to update its password, make sure both fields match
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1:
            if password2:
                if password1 != password2:
                    raise forms.ValidationError(_("Passwords don't match"))
            else:
                raise forms.ValidationError(_("You have to confirm your password"))

        return self.cleaned_data

    def save(self, *args, **kwargs):
        """
        Update the primary email address and the password on the
        related User object as well.
        """
        u = self.instance

        if self.cleaned_data.get('password1'):
            u.set_password(self.cleaned_data.get('password1'))
        u.save()
        account = super(AccountEditForm, self).save(*args,**kwargs)
        return account



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'genre', 'birthdate', 'email', 'country', 'timezone', 'town')

    birthdate = forms.DateField(label=_("Birthdate"),
                                widget=SelectDateWidget(years=range(datetime.date.today().year-10, 1900, -1))
                                )

    email = forms.EmailField(label=_("Email address"),
                             help_text='')

    genre = forms.ChoiceField(label=_("Genre"),
                              choices=(('', '----'),) + UserProfile.genre_choices,
                              widget=forms.Select(),
                              required=True)

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
        Update the primary email address and the password on the
        related User object as well.
        """
        u = self.instance.user

        if self.cleaned_data.get('password1'):
            u.set_password(self.cleaned_data.get('password1'))
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileEditForm, self).save(*args,**kwargs)
        return profile

