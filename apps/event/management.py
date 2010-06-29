from django.db.models import signals
from django.utils.translation import ugettext_noop as _

import notification.models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("gigbargain_new", _("New gig bargain"), _("you have received a gig bargain"))
    notification.create_notice_type("gigbargain_approved", _("Gig bargain approved"), _("A gig bargain was approved"))
    notification.create_notice_type("gigbargain_disapproved", _("Gig bargain disapproved"), _("A gig bargain was approved"))
    notification.create_notice_type("gigbargain_amended", _("Gig bargain amended"), _("A gig bargain was amended"))
    
signals.post_syncdb.connect(create_notice_types, sender=notification)

