from django import forms

from .models import FreetextPortlet

class FreetextPortletForm(forms.ModelForm):
    """
    Form for the FreetextPortlet.
    """
    class Meta:
        model = FreetextPortlet



