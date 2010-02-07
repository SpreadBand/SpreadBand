from django.contrib import admin

from .models import Band, BandRole, BandMember

from .myportlets import TextPortlet

admin.site.register((Band, BandRole, BandMember, TextPortlet))



