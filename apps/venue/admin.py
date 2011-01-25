from django.contrib import admin

from .models import Venue, VenuePicture, VenueMember, VenueRole

admin.site.register((Venue, VenuePicture, VenueMember, VenueRole))
