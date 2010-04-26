from django.contrib import admin

from .models import GigBargain, GigBargainBand

admin.site.register((GigBargainBand, GigBargain))


