import itertools
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, send_mass_mail
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.conf import settings

from presskit.models import PresskitViewRequest

class Command(BaseCommand):
    help = 'Send a reminder to the venues that still have pending presskit views'

    def handle(self, *args, **options):

        today = datetime.datetime.today()

        # We send a reminder to presskit that are younger than 30 days
        # old and had no activity during the 5 latest days
        thirty_days_ago = today - datetime.timedelta(days=30)
        seven_days_ago = today - datetime.timedelta(days=5)

        # Make a dict having as key the venue and value the pending gig requests
        request = PresskitViewRequest.objects.filter(state__in=('P', 'S'), modified_on__range=(thirty_days_ago, seven_days_ago)).order_by('venue')
        venues_to_remind = dict((k, list(v)) for k, v in itertools.groupby(request, lambda x: x.venue))

        # Prepare an email for each venue
        messages = []
        for venue, viewrequests in venues_to_remind.iteritems():
            message = (_("%(prefix)sReminder: You have pending gig requests for '%(venue_name)s'!" % {'prefix': settings.EMAIL_SUBJECT_PREFIX,
                                                                                                      'venue_name': venue.name}
                         ), 
                       render_to_string(template_name='presskit/venue_gigrequests_reminder.txt',
                                        dictionary={'venue': venue,
                                                    'viewrequests': viewrequests
                                                    },
                                        ),
                       settings.SERVER_EMAIL,
                       [member.email for member in venue.members.all()]
                       )

            messages.append(message)


        # Spam 'em all !
        send_mass_mail(messages, fail_silently=False)


            

