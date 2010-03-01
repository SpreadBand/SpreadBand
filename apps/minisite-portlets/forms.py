from django import forms

from .models import FreetextPortlet, TwitterPortlet

class FreetextPortletForm(forms.ModelForm):
    """
    Form for the FreetextPortlet.
    """
    class Meta:
        model = FreetextPortlet

class TwitterPortletForm(forms.ModelForm):
    """
    Form for the TwitterPortlet.
    """
    class Meta:
        model = TwitterPortlet
        exclude = ('title',)


