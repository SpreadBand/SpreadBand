from django import forms
from django.utils.translation import ugettext
_ = lambda u: unicode(ugettext(u))

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


from django_countries import countries
class VenueGeoSearchForm(forms.Form):
    country = forms.ChoiceField(label=_('Country'),
                                choices=(('', '----'),) + countries.COUNTRIES,
                                required=False)

    city = forms.CharField(label=_('City'),
                           required=False)

    distance = forms.IntegerField(label=_('Distance'),
                                  required=False,
                                  min_value=1,
                                  max_value=500,
                                  widget=forms.TextInput(attrs={'size': '5'}))

