from django import forms

from .models import Venue, VenuePicture

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'slug', 'ambiance', 'description')


class VenueUpdateForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zipcode', 'city', 'country', 'ambiance', 'capacity', 'description', 'video')


class VenuePictureForm(forms.ModelForm):
    class Meta:
        model = VenuePicture
        fields = ('original_image', 'title', 'description', 'is_avatar')

