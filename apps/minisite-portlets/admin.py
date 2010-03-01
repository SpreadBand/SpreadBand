from django.contrib import admin

from .models import FreetextPortlet, TwitterPortlet, AudioPlayerPortlet

admin.site.register((FreetextPortlet, TwitterPortlet, AudioPlayerPortlet))



