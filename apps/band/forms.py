from datetime import date
from django import forms
from django.utils.translation import ugettext as _

from utils.forms.widgets import MonthYearWidget

from .models import Band, BandMember, BandRole, BandPicture

class BandCreateForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('name', 'slug', 'city', 'zipcode', 'country')

class BandUpdateForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('name', 'founded_on', 'zipcode', 'city', 'country', 'genres', 'influences', 'biography', 'technical_sheet',)

    founded_on = forms.DateField(required=True,
                                 widget=MonthYearWidget(years=xrange(date.today().year-50, date.today().year+1))
                                 )

class BandMemberRequestForm(forms.ModelForm):
    class Meta:
        model = BandMember
        fields = ('roles',)

    def clean(self):
        value = self.cleaned_data.get('roles')

        if not value:
            raise forms.ValidationError(_("You must at least have a role"))

        return self.cleaned_data

class BandPictureForm(forms.ModelForm):
    class Meta:
        model = BandPicture
        fields = ('original_image', 'is_avatar')
    

from django.forms import CharField

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class BandMemberAddForm(forms.ModelForm):
    class Meta:
        model = BandMember
        fields = ('user', 'roles')
    
    user = CharField(max_length=50, 
                     help_text='Enter the username of the person to add')

    def clean_user(self):
        value = self.cleaned_data['user']
        try:
            user = User.objects.get(username__iexact=value)
        except User.DoesNotExist, e:
            raise forms.ValidationError(_("The user's nickname you have entered doesn't exist"))

        return user
    


from django_countries import countries
class BandGeoSearchForm(forms.Form):
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

