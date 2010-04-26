from django import forms

from .models import Band, BandMember, BandPicture

class BandCreateForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('name', 'slug')

class BandUpdateForm(forms.ModelForm):
    class Meta:
        model = Band

class BandMemberRequestForm(forms.ModelForm):
    class Meta:
        model = BandMember
        fields = ('role',)

class BandPictureForm(forms.ModelForm):
    class Meta:
        model = BandPicture
        fields = ('original_image',)
    


    


