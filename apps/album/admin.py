from django.contrib import admin

from .models import Album, Track, AlbumCover

admin.site.register((Album, Track, AlbumCover))



