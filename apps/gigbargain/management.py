from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

import notification.models as notification

from annoying.decorators import signals

@signals(post_syncdb, sender=notification)
def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("gigbargain_invitation", _("Gig bargain invitation"), _("you have received an invitation to play"))
    notification.create_notice_type("gigbargain_draft_ready", _("Gig bargain draft ready"), _("A gig bargain draft is ready"))
    notification.create_notice_type("gigbargain_failed", _("Gig bargain failed"), _("Negociations of a gig bargain failed"))
    notification.create_notice_type("gigbargain_concluded", _("Gig bargain concluded"), _("A gig bargain was concluded"))

    notification.create_notice_type("gigbargain_draft_submitted_to_venue", _("Draft submitted to venue"), _("A gig bargain draft was submitted to the venue"))

    
