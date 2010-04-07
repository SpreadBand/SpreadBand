from django import forms

from .models import Album, Track

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['band']

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track

class NewTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['file']



