from django.contrib import admin

from reversion.admin import VersionAdmin


from .models import GigBargain, GigBargainBand, Gig, GigBargainVenueState

class GigBargainBandAdminInline(admin.StackedInline):
    model = GigBargainBand
    extra = 0

class GigBargainAdmin(VersionAdmin):
    inlines = (GigBargainBandAdminInline,)

admin.site.register(Gig)
admin.site.register(GigBargain, GigBargainAdmin)
admin.site.register(GigBargainBand, VersionAdmin)
admin.site.register(GigBargainVenueState, VersionAdmin)




