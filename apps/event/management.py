from django.db.models import signals
from django.utils.translation import ugettext_noop as _

import notification.models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("new_gig_bargain", _("New gig bargain"), _("you have received a gig bargain"))
    
signals.post_syncdb.connect(create_notice_types, sender=notification)

