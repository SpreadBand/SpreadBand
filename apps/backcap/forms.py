from django.forms import ModelForm
from django.forms import CharField, HiddenInput, ChoiceField
from django.forms import RadioSelect

from .models import Feedback

class FeedbackNewForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('kind', 'title', 'text', 'referer')

    referer = CharField(widget=HiddenInput, required=False)
    kind = ChoiceField(widget=RadioSelect(), choices=Feedback.KIND_CHOICES)
    

class FeedbackEditForm(ModelForm):
    class Meta:
        model = Feedback

