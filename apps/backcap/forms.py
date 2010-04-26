from django.forms import ModelForm
from django.forms import CharField, HiddenInput

from .models import Feedback, Vote

class FeedbackNewForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('kind', 'title', 'text', 'referer')

    referer = CharField(widget=HiddenInput, required=False)

class FeedbackEditForm(ModelForm):
    class Meta:
        model = Feedback

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ('choice',)
