from django import forms
from .models import PressKit

from media.models import Track

class PressKitVideoForm(forms.ModelForm):
    class Meta:
        model = PressKit
        fields = ('video',)

class PressKitTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('title', 'file')





