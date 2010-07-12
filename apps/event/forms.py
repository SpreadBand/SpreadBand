from django import forms
from django.forms import formsets
from django.forms import ModelChoiceField, ChoiceField
from django.utils.translation import ugettext as _

# from schedule.forms import SpanForm

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

from durationfield.forms.fields import DurationField

from utils.forms.fields import RangeField
from utils.forms.widgets import RangeWidget, SliderRangeWidget

from .models import Gig, GigBargain, GigBargainBand

from venue.models import Venue

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


class GigBargainForBandForm(forms.ModelForm):
    """
    What a band can edit on a gig bargain
    """
    class Meta:
        model = GigBargain
        fields = ('access', 'fee_amount', 'remuneration')

    access = ChoiceField(choices=[['', "(Pick one)"]] + GigBargain.ACCESS_CHOICES,
                         required=True
                         )

    remuneration = ChoiceField(choices=[['', "(Pick one)"]] + GigBargain.REMUNERATION_CHOICES,
                               required=True
                               )


class GigBargainForVenueForm(forms.ModelForm):
    """
    What a venue can edit on a gig bargain
    """
    class Meta:
        model = GigBargain
        fields = ('opens_at', 'closes_at', 'access', 'fee_amount', 'remuneration')

    access = ChoiceField(choices=[['', "(Let the bands choose)"]] + GigBargain.ACCESS_CHOICES,
                         required=False
                         )

    remuneration = ChoiceField(choices=[['', "(Let the bands choose)"]] + GigBargain.REMUNERATION_CHOICES,
                               required=False
                               )



class GigBargainNewFromVenueForm(forms.ModelForm):
    class Meta:
        model = GigBargain
        fields = ('date', 'opens_at', 'closes_at', 'venue', 'access', 'fee_amount', 'remuneration')

    def __init__(self, aUser, *args, **kwargs):
        self.user = aUser
        forms.ModelForm.__init__(self, *args, **kwargs)

    # XXX: Filter here and display only our owned venues
    venue = ModelChoiceField(queryset=Venue.objects.all())

    access = ChoiceField(choices=[['', "(Let the bands choose)"]] + GigBargain.ACCESS_CHOICES,
                         required=False
                         )

    remuneration = ChoiceField(choices=[['', "(Let the bands choose)"]] + GigBargain.REMUNERATION_CHOICES,
                               required=False
                               )
    


class GigBargainBandPartEditForm(forms.ModelForm):
    """
    When a band edits its part
    """
    class Meta:
        model = GigBargainBand
        fields = ('starts_at', 'set_duration', 'eq_starts_at', 'percentage', 'amount', 'defrayment')

    starts_at = forms.TimeField(required=True)
    set_duration = DurationField(required=True)
    percentage = forms.IntegerField(min_value=0, max_value=100)

class GigBargainBandForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        fields = ('band', 'starts_at', 'set_duration', 'eq_starts_at', 'percentage', 'amount', 'defrayment')

    percentage = forms.IntegerField(min_value=0, max_value=100, initial=0)

class BaseGigBargainBandFormSet(formsets.BaseFormSet):
    def clean(self):
        """
        Make sure we don't have two times the same band.
        Also make sure we have at least one band.
        """
        if any(self.errors):
            return

        # Check we have at least one band
        if not self.forms[0].cleaned_data.has_key('band'):
            raise forms.ValidationError(_("There must be at least one band"))

        # Check multiple bands
        bands = []
        for i in range(0, self.total_form_count()):
            form = self.forms[i]

            # If this form was not bound
            if form.cleaned_data == {}:
                continue

            band = form.cleaned_data['band']
            if band in bands:
                raise forms.ValidationError, _("Bands in a bargain must be distincts")

            bands.append(band)
        

    # band = AutoCompleteSelectField('band', required=True)
    
