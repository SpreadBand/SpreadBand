from django.db import models
from django.db.models import ForeignKey, CharField, TextField, DateTimeField
from django.db.models import PositiveIntegerField, BooleanField, IntegerField
from django.contrib.auth.models import User

class Feedback(models.Model):
    KIND_CHOICES = (
        ('Q', 'Question'),
        ('P', 'Problem'),
        ('I', 'Idea'),
        )

    STATUS_CHOICES = (
        ('O', 'Opened'),
        ('A', 'Assigned'),
        ('W', 'Won\'t Fix'),
        ('R', 'Re-opened'),
        ('C', 'Closed'),
        )

    # Timestamps
    created_on = DateTimeField(auto_now_add=True)
    modified_on = DateTimeField(auto_now=True)

    # Who and what
    user = ForeignKey(User)
    referer = TextField()

    # Contents
    kind = CharField(max_length=1, choices=KIND_CHOICES)
    title = CharField(max_length=255)
    text = TextField()

    # State
    status = CharField(max_length=1, choices=STATUS_CHOICES, default='O')

    # Votes
    vote_for = PositiveIntegerField(default=0)
    vote_against = PositiveIntegerField(default=0)
    vote_balance = IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.kind, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('backcap:feedback-detail', (self.id,))
    

class Vote(models.Model):
    """
    A vote for a Feedback
    """
    user = ForeignKey(User, related_name='feedback_votes')
    feedback = ForeignKey(Feedback, related_name='votes')
    choice = BooleanField()

    def __unicode__(self):
        return "%s - %s - %s" % (self.feedback.title,
                                 self.user.username,
                                 self.choice)
