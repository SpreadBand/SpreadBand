from django import forms

from .models import GigPlace

class GigPlaceForm(forms.ModelForm):
    class Meta:
        model = GigPlace
        exclude = ('calendar', 'photos')



