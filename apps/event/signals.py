import django.dispatch

gigbargain_concluded = django.dispatch.Signal()
gigbargain_new_from_venue = django.dispatch.Signal(providing_args=['aGigBargain'])





