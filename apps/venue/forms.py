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

    distance = forms.FloatField(label=_('Distance'),
                                required=False,
                                initial=5.0,
                                min_value=1.0,
                                max_value=10000.0,
                                widget=forms.HiddenInput()
                                )


    circle_x = forms.FloatField(label=_('X'),
                                initial=0.0,
                                required=False,
                                widget=forms.HiddenInput()
                                )
    
    circle_y = forms.FloatField(label=_('Y'),
                                required=False,
                                initial=0.0,
                                widget=forms.HiddenInput()
                                )
                                  
               
from tagging.forms import TagField
            
class NewCantFindForm(forms.Form):
    distance = forms.FloatField(required=True,
                                widget=forms.HiddenInput())
    x = forms.FloatField(required=True,
                         widget=forms.HiddenInput())
    y = forms.FloatField(required=True,
                         widget=forms.HiddenInput())

    ambiance = TagField(required=True,
                        widget=forms.HiddenInput())

class SendNewCantFindForm(NewCantFindForm):
    message = forms.CharField(required=False,
                              widget=forms.Textarea())
