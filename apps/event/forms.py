from django import forms

# from schedule.forms import SpanForm

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

from utils.forms.fields import RangeField
from utils.forms.widgets import RangeWidget, SliderRangeWidget

from .models import Gig, GigBargain, GigBargainBand

class GigCreateForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ('venue', 'event_date', 'start_time', 'end_time', 'bands', 'title', 'description',)
    
    bands = AutoCompleteSelectMultipleField('band', required=True)
    venue = AutoCompleteSelectField('venue', required=True)

class GigBargainForm(forms.ModelForm):
    class Meta:
        model = GigBargain
        fields = ('date', 'opens_at', 'closes_at', 'venue', 'access', 'fee_amount')

    venue = AutoCompleteSelectField('venue', required=True)


class GigBargainBandForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        exclude = ('bargain',)

    # band = AutoCompleteSelectField('band', required=True)
    
