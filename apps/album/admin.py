from django.contrib import admin

from .models import Album, Track

admin.site.register((Album, Track))



