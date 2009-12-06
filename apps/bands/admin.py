from django.contrib import admin

from .models import Band, BandRole, BandMember

admin.site.register((Band, BandRole, BandMember))



