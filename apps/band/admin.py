from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Band, BandRole, BandMember, BandPicture

class BandAdmin(VersionAdmin):
    pass

admin.site.register(Band, BandAdmin)

admin.site.register((BandRole, BandMember, BandPicture))



