from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

import notification.models as notification

from annoying.decorators import signals

@signals(post_syncdb, sender=notification)
def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("gigbargain_proposal", _("New gig bargain proposal"), _("you have received a proposal for a gig bargain"))
    notification.create_notice_type("gigbargain_new", _("New gig bargain"), _("you have received a gig bargain"))
    notification.create_notice_type("gigbargain_approved", _("Gig bargain approved"), _("A gig bargain was approved"))
    notification.create_notice_type("gigbargain_disapproved", _("Gig bargain disapproved"), _("A gig bargain was approved"))
    notification.create_notice_type("gigbargain_amended", _("Gig bargain amended"), _("A gig bargain was amended"))
    notification.create_notice_type("gigbargain_concluded", _("Gig bargain concluded"), _("A gig bargain was concluded"))
    
