from django import forms

from registration.forms import RegistrationFormTermsOfService
from tagging.forms import TagField

from band.forms import BandCreateForm
from band.models import BandRole

class UserBandRegistrationForm(RegistrationFormTermsOfService):
    """
    A form to register a band AND a user
    """
    band_name = forms.CharField(max_length=200)
    band_slug = forms.SlugField(max_length=40)
    band_tags = TagField()

    user_band_roles = forms.ModelMultipleChoiceField(queryset=BandRole.objects)


    def clean_band_slug(self):
        """
        Make sure this slug doesn't exist yet
        """
        value = self.cleaned_data['band_slug']
        return value


