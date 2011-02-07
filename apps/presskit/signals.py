import django.dispatch

presskitview_new = django.dispatch.Signal()

presskitview_band_comment = django.dispatch.Signal()
presskitview_venue_comment = django.dispatch.Signal()

presskitview_accepted_by_venue = django.dispatch.Signal()
presskitview_refused_by_venue = django.dispatch.Signal()






