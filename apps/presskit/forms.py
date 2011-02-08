from django import forms
from django.utils.translation import ugettext as _
from .models import PressKit, PresskitViewRequest

from media.models import Track

class PressKitVideoForm(forms.ModelForm):
    class Meta:
        model = PressKit
        fields = ('video',)

class PressKitTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('title', 'file', 'has_rights')

    has_rights = forms.BooleanField(label=_("I have all the rights to upload this track"),
                                    help_text=_("By checking this box, you certify that you have the rights to upload this track and that you are not belonging to a company that denies this."),
                                    required=True)

class PresskitViewRequestForm(forms.ModelForm):
    class Meta:
        model = PresskitViewRequest
        fields = ('message',)

    message = forms.CharField(widget=forms.Textarea,
                              required=False)

