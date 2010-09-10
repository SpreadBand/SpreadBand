from django import forms
from .models import PressKit

class PressKitVideoForm(forms.ModelForm):
    class Meta:
        model = PressKit
        fields = ('video',)





