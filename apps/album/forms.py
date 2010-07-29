from django import forms

from .models import Album, AlbumTrack, AlbumCover

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('band',)

class TrackForm(forms.ModelForm):
    class Meta:
        model = AlbumTrack

class NewTrackForm(forms.ModelForm):
    class Meta:
        model = AlbumTrack
        fields = ('file',)

class AlbumCoverForm(forms.ModelForm):
    class Meta:
        model = AlbumCover
        fields = ('original_image',)

