from django.contrib import admin

from .models import GigBargain, GigBargainBand, Gig

admin.site.register((GigBargainBand, GigBargain, Gig))


