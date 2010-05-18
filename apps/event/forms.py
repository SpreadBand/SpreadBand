from django import forms

# from schedule.forms import SpanForm

from .models import Gig, GigBargain, GigBargainBand

class GigCreateForm(forms.ModelForm):
    class Meta:
        model = Gig
        # fields = ('venue', 'start', 'end', 'bands', 'title', 'description',)

class GigBargainForm(forms.ModelForm):
    class Meta:
        model = GigBargain
        fields = ('date', 'opens_at', 'closes_at', 'venue', 'access', 'fee_amount')

class GigBargainBandForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        exclude = ('bargain',)
