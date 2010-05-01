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
            user = User.objects.get(username=value)
        except User.DoesNotExist, e:
            raise forms.ValidationError(_("The user's nickname you have entered doesn't exist"))

        return user
    


