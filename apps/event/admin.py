from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Gig

admin.site.register(Gig)




