from django.contrib import admin

from .models import Venue, VenuePicture

admin.site.register((Venue, VenuePicture))
