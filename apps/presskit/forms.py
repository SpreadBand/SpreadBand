from django import forms
from .models import PressKit, PresskitViewRequest

from media.models import Track

class PressKitVideoForm(forms.ModelForm):
    class Meta:
        model = PressKit
        fields = ('video',)

class PressKitTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('title', 'file')

class PresskitViewRequestForm(forms.ModelForm):
    class Meta:
        model = PresskitViewRequest
        fields = ('message',)

    message = forms.CharField(widget=forms.Textarea,
                              required=False)

