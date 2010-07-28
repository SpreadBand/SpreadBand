from django import forms
from django.forms import formsets
from django.forms import ModelChoiceField, ChoiceField
from django.utils.translation import ugettext as _

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

from .models import Gig

class GigCreateForm(forms.ModelForm):
    """
    Form to create a new gig
    """
    class Meta:
        model = Gig
        fields = ('venue', 'event_date', 'start_time', 'end_time', 'bands', 'title', 'description',)
    
    bands = AutoCompleteSelectMultipleField('band', required=True)
    venue = AutoCompleteSelectField('venue', required=True)

    
