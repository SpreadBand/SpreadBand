from django.views.generic.date_based import archive_today

from event.models import Gig

def gigs_today(request):
    """
    Display gigs of the day
    """
    return archive_today(request,
                         queryset=Gig.objects.all(),
                         date_field='event_date',
                         allow_empty=True,
                         template_name='event/gigs_today.html',
                         template_object_name='gig',
                         allow_future=True)
