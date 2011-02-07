from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

import notification.models as notification

from annoying.decorators import signals

@signals(post_syncdb, sender=notification)
def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("presskitview_band_comment", _("band comment on presskit"), _("A band has commented a presskit view request"))
    notification.create_notice_type("presskitview_venue_comment", _("venue comment on presskit"), _("A venue has commented a presskit view request"))

    notification.create_notice_type("presskitview_accepted_by_venue", _("venue accepted to setup a gig"), _("A venue has accepted to set up a gig"))
    notification.create_notice_type("presskitview_refused_by_venue", _("venue refused to setup a gig"), _("A venue has refused to set up a gig"))

    notification.create_notice_type("presskitview_new", _("band proposed to set up gig to a venue"), _("A band has proposed to set up a gig"))

    
