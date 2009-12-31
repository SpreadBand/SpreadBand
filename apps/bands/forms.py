from django import forms

from .models import Band, BandMember

class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        exclude = ('calendar', 'photos')

class BandMemberRequestForm(forms.ModelForm):
    class Meta:
        model = BandMember
        exclude = ('user', 'approved')

    


    


