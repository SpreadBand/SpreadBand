from django import forms

from .models import Album, Track, AlbumCover

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('band',)

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track

class NewTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('file',)

class AlbumCoverForm(forms.ModelForm):
    class Meta:
        model = AlbumCover
        fields = ('original_image',)



