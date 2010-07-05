from django import forms

from .models import Venue

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        exclude = ('calendar', 'photos')


class VenueUpdateForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'slug', 'ambiance', 'description')
