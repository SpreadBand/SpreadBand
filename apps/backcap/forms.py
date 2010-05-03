from django.forms import ModelForm
from django.forms import CharField, HiddenInput

from .models import Feedback

class FeedbackNewForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('kind', 'title', 'text', 'referer')

    referer = CharField(widget=HiddenInput, required=False)

class FeedbackEditForm(ModelForm):
    class Meta:
        model = Feedback

