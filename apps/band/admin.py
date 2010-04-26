from django.contrib import admin

from .models import Band, BandRole, BandMember, BandPicture

admin.site.register((Band, BandRole, BandMember, BandPicture))



