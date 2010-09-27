from django import forms
from django.forms import formsets
from django.forms import ModelChoiceField, ChoiceField
from django.utils.translation import ugettext as _

# from schedule.forms import SpanForm

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

# from durationfield.forms.fields import DurationField
from timedelta.forms import TimedeltaFormField

from venue.models import Venue

from .models import GigBargain, GigBargainBand

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
        fields = ('access', 'fee_amount')

    access = ChoiceField(label=_('Access type'),
                         choices=[['', _("(Pick one)")]] + GigBargain.ACCESS_CHOICES,
                         required=True
                         )


class GigBargainForVenueForm(forms.ModelForm):
    """
    What a venue can edit on a gig bargain
    """
    class Meta:
        model = GigBargain
        fields = ('opens_at', 'closes_at', 'access', 'fee_amount', 'remuneration')

    opens_at = forms.TimeField(required=True)
    closes_at = forms.TimeField(required=True)

    access = ChoiceField(label=_('Access type'),
                         choices=[['', _("(Let the bands choose)")]] + GigBargain.ACCESS_CHOICES,
                         required=False
                         )

    remuneration = ChoiceField(label=_('Remuneration'),
                               choices=[['', _("(Let the bands choose)")]] + GigBargain.REMUNERATION_CHOICES,
                               required=False
                               )


class GigBargainNewForm(forms.ModelForm):
    """
    Generic form to create a gig bargain
    """
    def __init__(self, aUser, *args, **kwargs):
        self.user = aUser
        forms.ModelForm.__init__(self, *args, **kwargs)

    def clean_date(self):
        # Make sure this is a date in the future
        date = self.cleaned_data.get('date')
        if date < date.today():
            raise forms.ValidationError(_("Date must be in the future, or today"))
        return date

    def clean(self):
        # Make sure we give a cost if the access is not set to free
        access = self.cleaned_data.get('access')
        fee_amount = self.cleaned_data.get('fee_amount')
        if access and access != 'FREE':
            if fee_amount in (0, None):
                raise forms.ValidationError("You need to provide a cost, since the access is not free")

        return self.cleaned_data

    # XXX: Filter here and display only our owned venues
    venue = ModelChoiceField(queryset=Venue.objects.all())



class GigBargainNewFromVenueForm(GigBargainNewForm):
    """
    Form to create a gig bargain, for Venues
    """
    class Meta:
        model = GigBargain
        fields = ('date', 'opens_at', 'closes_at', 'venue', 'access', 'fee_amount', 'remuneration')

    access = ChoiceField(label=_('Access type'),
                         choices=[['', _("(Let the bands choose)")]] + GigBargain.ACCESS_CHOICES,
                         required=False
                         )

    remuneration = ChoiceField(label=_('Remuneration'),
                               choices=[['', _("(Let the bands choose)")]] + GigBargain.REMUNERATION_CHOICES,
                               required=False
                               )



class GigBargainNewFromBandForm(GigBargainNewForm):
    """
    Form to create a gig bargain, for Bands
    """
    class Meta:
        model = GigBargain
        fields = ('date', 'venue', 'access', 'fee_amount', 'remuneration')

    access = ChoiceField(label=_('Access type'),
                         choices=[['', _("(Let the venue choose)")]] + GigBargain.ACCESS_CHOICES,
                         required=False,
                         )

    remuneration = ChoiceField(label=_('Remuneration'),
                               choices=[['', _("(Let the venue choose)")]] + GigBargain.REMUNERATION_CHOICES,
                               required=False,
                               )




class GigBargainNewFullForm(forms.ModelForm):
    """
    Used to check wether we have all information or only a partial set
    """
    class Meta:
        model = GigBargain
        fields = ('date', 'venue', 'access', 'fee_amount', 'remuneration')

    date = forms.DateField(required=True)
    access = ChoiceField(label=_('Access type'),
                         choices=GigBargain.ACCESS_CHOICES,
                         required=True
                         )

    remuneration = ChoiceField(label=_('Remuneration'),
                               choices=GigBargain.REMUNERATION_CHOICES,
                               required=True
                               )
    

class GigBargainBandForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        fields = ('band', 'starts_at', 'set_duration', 'eq_starts_at', 'percentage', 'amount', 'defrayment')

    percentage = forms.IntegerField(label=_('Percentage'),
                                    required=False,
                                    min_value=0, max_value=100, initial=0)
    starts_at = forms.TimeField(label=_('Starts at'),
                                input_formats=('%H:%M:%S', '%H:%M', '%Hh%M', '%H'), required=False)
    eq_starts_at = forms.TimeField(label=_('Equalisation starts at'),
                                   input_formats=('%H:%M:%S', '%H:%M', '%Hh%M', '%H'), required=False)

    def clean(self):
        # Make sure the equalization isn't after the beginning of the set
        equalization = self.cleaned_data.get('eq_starts_at')
        starts_at = self.cleaned_data.get('starts_at')
        if equalization:
            if starts_at <= equalization:
                raise forms.ValidationError(_("Equalizations must start before the gig itself"))

        return self.cleaned_data


class GigBargainBandPartEditForm(GigBargainBandForm):
    """
    When a band edits its part
    """
    class Meta:
        model = GigBargainBand
        fields = ('starts_at', 'set_duration', 'eq_starts_at', 'percentage', 'amount', 'defrayment')

    starts_at = forms.TimeField(input_formats=('%H:%M:%S', '%H:%M', '%Hh%M',  '%H'), required=True)
    set_duration = TimedeltaFormField(label=_('Set duration'),
                                      required=True)


class GigBargainMyBandForm(GigBargainBandForm):
    class Meta:
        model = GigBargainBand
        fields = ('starts_at', 'set_duration', 'eq_starts_at', 'percentage', 'amount', 'defrayment')

    percentage = forms.IntegerField(label=_('Percentage'),
                                    min_value=0, max_value=100, initial=0, required=False)
    set_duration = TimedeltaFormField(label=_('Set duration'),
                                      required=True)

class GigBargainMyBandFullForm(GigBargainMyBandForm):
    def __init__(self, aGigBargain, *args, **kwargs):
        self._gigbargain = aGigBargain
        GigBargainMyBandForm.__init__(self, *args, **kwargs)

    starts_at = forms.TimeField(required=True)

    def clean(self):
        percentage = self.cleaned_data.get('percentage')
        amount = self.cleaned_data.get('amount')

        if self._gigbargain.remuneration == 'PERC':
            if not percentage or percentage == 0:
                raise forms.ValidationError(_("Percentage is missing"))

        elif self._gigbargain.remuneration == 'FIXE':
            if not amount or amount == 0:
                raise forms.ValidationError(_("Remuneration amount is missing"))

        return self.cleaned_data


class GigBargainBandInviteForm(GigBargainBandForm):
    def __init__(self, aGigBargain, *args, **kwargs):
        self._gigbargain = aGigBargain
        GigBargainBandForm.__init__(self, *args, **kwargs)
        
    def clean(self):
        cleaned_data = self.cleaned_data

        gigbargainband = None
        # Look up the band we want to add
        try:
            res = self._gigbargain.gigbargainband_set.get(band=cleaned_data.get('band'))
        except GigBargainBand.DoesNotExist:
            pass

        if gigbargainband:
            if gigbargainband.state == 'kicked':
                raise forms.ValidationError(_("You can't invite this band, it has been kicked"))
            else:
                raise forms.ValidationError(_("This band is already in this bargain"))

        return cleaned_data


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
    
class GigBargainBandRefuseForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        fields = ('reason',)

    reason = forms.CharField(required=True,
                             widget=forms.Textarea)


class VenueReasonForm(forms.ModelForm):
    class Meta:
        model = GigBargain
        fields = ('venue_reason',)

    venue_reason = forms.CharField(required=True,
                                   widget=forms.Textarea)


#-- Ajax forms
class GigBargainBandTimelineForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        fields = ('starts_at', 'set_duration', 'eq_starts_at')

class GigBargainBandRemunerationForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        fields = ('percentage', 'amount')

class GigBargainBandDefraymentForm(forms.ModelForm):
    class Meta:
        model = GigBargainBand
        fields = ('defrayment',)

#-- comments
from threadedcomments.forms import ThreadedCommentForm
class SectionComment(ThreadedCommentForm):
    comment = forms.CharField(max_length=300)
