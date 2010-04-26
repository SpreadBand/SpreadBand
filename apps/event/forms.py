from django import forms

from schedule.forms import EventForm

from .models import Gig, GigBargain, GigBargainBand

class GigForm(forms.ModelForm):
    class Meta:
        model = Gig

class GigBargainForm(forms.ModelForm):
    class Meta:
        model = GigBargain
        fields = ('date', 'opens_at', 'closes_at', 'venue', 'access', 'fee_amount')

class GigBargainBandForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        exclude = ('bargain',)
