from django.contrib import admin

from .models import Album, AlbumTrack, AlbumCover

admin.site.register((Album, AlbumTrack, AlbumCover))



